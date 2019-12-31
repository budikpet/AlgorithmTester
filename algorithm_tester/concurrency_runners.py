import os
import timeit
import time
import multiprocessing
import concurrent.futures
from enum import Enum
from typing import IO, Dict, List
from algorithm_tester_common.tester_dataclasses import AlgTesterContext, Algorithm, Parser
from algorithm_tester.plugins import plugins


new_template = """
def inner(_it, _timer{init}):
    {setup}
    _t0 = _timer()
    for _i in _it:
        ret_val = {stmt}
    _t1 = _timer()
    return _t1 - _t0, ret_val
"""
timeit.template = new_template

def get_click_options(context: AlgTesterContext, algorithm: Algorithm) -> Dict[str, object]:
    """
    Create a dictionary of options and arguments given to the Click CLI. 
    Used by Parser to generate name of the output file.
    
    Arguments:
        context {AlgTesterContext} -- [description]
        algorithm {Algorithm} -- [description]
    
    Returns:
        Dict[str, object] -- [description]
    """
    click_options: Dict[str, object] = context.get_options()
    click_options["algorithm_name"] = algorithm.get_name()
    click_options["algorithm"] = algorithm

    return click_options

def create_columns_description_file(context: AlgTesterContext, algorithm: Algorithm):
    """
    Create an output file with names of columns for a specific algorithm.
    
    Args:
        algorithm (str): Name of the algorithm whose columns are persisted.
        output_dir (str): Output directory.
    """
    column_descriptions = algorithm.get_columns()

    with open(f'{context.output_dir}/column_description_{algorithm.get_name()}.dat', "w") as f:
        f.write(f'{" ".join(column_descriptions)}\n')

class Runner(object):

    def compute_results(self, context: AlgTesterContext, files_dict: Dict[str, str]):
        pass

class BaseRunner(Runner):
    """
    Processes files and their instances sequentially. No concurrency is used.
    """

    def get_solution_for_instance(self, context: AlgTesterContext, algorithm: Algorithm, parsed_instance_data: Dict[str, object]) -> Dict[str, object]:
        if context.check_time:
            # Use timeit to get time
            t = timeit.Timer(lambda: algorithm.perform_algorithm(context, parsed_instance_data))
            elapsed_time, solution = t.timeit(number=context.time_retries)
            solution["elapsed_time"] = round((elapsed_time*1000)/context.time_retries, 10)   # Store in millis
        else:
            solution = algorithm.perform_algorithm(context, parsed_instance_data)

        return solution

    def get_parsed_instances_data(self, context: AlgTesterContext, input_file: IO, parser: Parser, algorithm: Algorithm) -> Dict[str, object]:
        """
        Parses instances from the input file.
        
        Arguments:
            context {AlgTesterContext} -- [description]
            input_file {IO} -- The opened input file.
            parser {Parser} -- [description]
            algorithm {Algorithm} -- [description]
        
        Yields:
            Dict[str, object] -- One parsed instance from the input file.
        """
        parsed_instance_data = parser.get_next_instance(input_file)
        
        click_options: Dict[str, object] = get_click_options(context, algorithm)
        
        output_file_name: str = parser.get_output_file_name(context, input_file, click_options)

        while parsed_instance_data is not None:
            parsed_instance_data["output_file_name"] = output_file_name
            parsed_instance_data["algorithm_name"] = algorithm.get_name()
            parsed_instance_data["algorithm"] = algorithm
            parsed_instance_data.update(context.extra_options)

            yield parsed_instance_data

            parsed_instance_data = parser.get_next_instance(input_file)

    def run_tester_for_file(self, context: AlgTesterContext, input_file_path: str):
        """
        Compute results for the given input file.
        
        Arguments:
            context {AlgTesterContext} -- [description]
            input_file_path {str} -- Path to the input file to compute results for.
        """
        parser: Parser = plugins.get_parser(context.parser_name)
        
        print(f'Currently testing file \'{input_file_path.split("/")[-1]}\'. Started {time.strftime("%H:%M:%S %d.%m.")}')
        with open(input_file_path, "r") as input_file:
            for algorithm_name in context.algorithm_names:
                algorithm: Algorithm = plugins.get_algorithm(algorithm_name)
                
                click_options = get_click_options(context, algorithm)
                output_file_name: str = parser.get_output_file_name(context, input_file, click_options)

                create_columns_description_file(context, algorithm)
                with open(f'{context.output_dir}/{output_file_name}', "w") as output_file:

                    for parsed_instance_data in self.get_parsed_instances_data(context, input_file, parser, algorithm):
                        solution = self.get_solution_for_instance(context, algorithm, parsed_instance_data)

                        parser.write_result_to_file(output_file, solution)

    def compute_results(self, context: AlgTesterContext, files_dict: Dict[str, str]):
        """
        Parses instances from given input files, solve them using required algorithms and write results to the output file.
        
        Arguments:
            context {AlgTesterContext} -- [description]
            files_dict {Dict[str, str]} -- All files with instances that are to be computed. 
            Keys were created to make it possible to process files in a sorted order.
        """
        for index, n_key in enumerate(sorted(files_dict)):
            if context.max_num is not None and index >= context.max_num:
                break

            input_file_path: str = files_dict.get(n_key)
            self.run_tester_for_file(context, input_file_path)

class ConcurrentFilesRunner(Runner):
    """
    Processes multiple files concurrently. Instances in each file is processed sequentially.
    
    """
    _base_runner: BaseRunner = BaseRunner()

    def compute_results(self, context: AlgTesterContext, files_dict: Dict[str, str]):
        """
        Parses instances from given input files, solve them using required algorithms and write results to the output file.
        
        Arguments:
            context {AlgTesterContext} -- [description]
            files_dict {Dict[str, str]} -- All files with instances that are to be computed. 
            Keys were created to make it possible to process files in a sorted order.
        """
        with concurrent.futures.ProcessPoolExecutor() as executor:
            for index, n_key in enumerate(sorted(files_dict)):
                if context.max_num is not None and index >= context.max_num:
                    break

                input_file_path: str = files_dict.get(n_key)
                executor.submit(self._base_runner.run_tester_for_file, context, input_file_path)

class ConcurrentInstancesRunner(Runner):
    """
    Processes multiple instances of 1 file concurrently.
    
    """
    _base_runner: BaseRunner = BaseRunner()

    def compute_solution_for_file_and_algorithm(self, context: AlgTesterContext, input_file: IO, parser: Parser, algorithm: Algorithm, executor: concurrent.futures.ProcessPoolExecutor):
        click_options = get_click_options(context, algorithm)
        output_file_name: str = parser.get_output_file_name(context, input_file, click_options)

        create_columns_description_file(context, algorithm)
        with open(f'{context.output_dir}/{output_file_name}', "w") as output_file:
            it = self._base_runner.get_parsed_instances_data(context, input_file, parser, algorithm)
            futures = [executor.submit(self._base_runner.get_solution_for_instance, context, algorithm, instance) for instance in it]

            # Get results
            for future in concurrent.futures.as_completed(futures):
                solution: Dict[str, object] = future.result()
                parser.write_result_to_file(output_file, solution)

    def run_tester_for_file(self, context: AlgTesterContext, input_file_path: str, executor: concurrent.futures.ProcessPoolExecutor):
        parser: Parser = plugins.get_parser(context.parser_name)
        
        print(f'Currently testing file \'{input_file_path.split("/")[-1]}\'. Started {time.strftime("%H:%M:%S %d.%m.")}')
        with open(input_file_path, "r") as input_file:
            for algorithm_name in context.algorithm_names:
                algorithm: Algorithm = plugins.get_algorithm(algorithm_name)
                
                self.compute_solution_for_file_and_algorithm(context, input_file, parser, algorithm, executor)

    def compute_results(self, context: AlgTesterContext, files_dict: Dict[str, str]):
        """
        Parses instances from given input files, solve them using required algorithms and write results to the output file.
        
        Arguments:
            context {AlgTesterContext} -- [description]
            files_dict {Dict[str, str]} -- All files with instances that are to be computed. 
            Keys were created to make it possible to process files in a sorted order.
        """
        with concurrent.futures.ProcessPoolExecutor() as executor:

            for index, n_key in enumerate(sorted(files_dict)):
                if context.max_num is not None and index >= context.max_num:
                    break

                input_file_path: str = files_dict.get(n_key)
                self.run_tester_for_file(context, input_file_path, executor)

class Runners(Enum):
    """
    Contains references to all Concurrency runners available.
    
    Arguments:
        Enum {Runner} -- A concurrency runner.
    """
    BASE = BaseRunner()
    FILES = ConcurrentFilesRunner()
    INSTANCES = ConcurrentInstancesRunner()