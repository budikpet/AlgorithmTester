import os
import timeit
import time
import multiprocessing
import concurrent.futures
from enum import Enum
from typing import IO, Dict, List
from algorithm_tester_common.tester_dataclasses import AlgTesterContext, Algorithm, Parser, Communicator
from algorithm_tester.plugins import plugins
from algorithm_tester.helpers import curr_time_millis

"""
Contains logic of all concurrency runners. These provide logic of the application with different types of concurrency.
"""

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
        context {AlgTesterContext} -- Current application context.
        algorithm {Algorithm} -- Currently tested algorithm.
    
    Returns:
        Dict[str, object] -- Dictionary with data that the algorithm additionally needs to identify the output file name.
    """
    click_options: Dict[str, object] = context.get_options()
    click_options["algorithm_name"] = algorithm.get_name()
    click_options["algorithm"] = algorithm

    return click_options

def get_communicators(context: AlgTesterContext):
    """
    Prepares and returns a list of Communicator instances.
    
    Arguments:
        context {AlgTesterContext} -- [description]
    
    Returns:
        List[Communicator] -- List of Communicator instances.
    """
    communicators: List[Communicator] = list()
    for communicator_name in context.communicator_names:
        communicator: Communicator = plugins.get_communicator(communicator_name)
        communicators.append(communicator)

    return communicators

# def notify_communicators(context: AlgTesterContext, communicators: List[Communicator], output_file_name: str) -> bool:
#     """
#     Notifies all Communicators that a instance was computed if enough time has passed since the last notification.
    
#     Arguments:
#         context {AlgTesterContext} -- Used context.
#         communicators {List[Communicator]} -- All available communicators.
#         output_file_name {str} -- Name of the output file that was created.

#     Returns:
#         Bool -- True if communicators were notified, False if not
#     """
#     curr_time: float = curr_time_millis()

#     if (curr_time - _LAST_COMM_TIME.value) >= context.min_time_between_communications:
#         # Notify communicators
#         with _LAST_COMM_TIME.get_lock():
#             print(f'before: {curr_time} - {_LAST_COMM_TIME.value}')
#             _LAST_COMM_TIME.value = curr_time
#             print(f'after: {curr_time} - {_LAST_COMM_TIME.value}')

#         for communicator in communicators:
#             communicator.notify_instance_computed(context, output_file_name, _COUNTER.value)

#         return True

#     return False

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

    def compute_results(self, context: AlgTesterContext, input_files: List[str]):
        pass

class BaseRunner(Runner):
    """
    Processes files and their instances sequentially. No concurrency is used.
    """

    def get_solution_for_instance(self, context: AlgTesterContext, algorithm: Algorithm, parsed_instance_data: Dict[str, object]) -> Dict[str, object]:
        """
        Invoke the selected algorithm's perform_algorithm method on the parsed instance data.
        
        Arguments:
            context {AlgTesterContext} -- Current application context.
            algorithm {Algorithm} -- Currently tested algorithm.
            parsed_instance_data {Dict[str, object]} -- Instance data of 1 instance parsed from the instance file.
        
        Returns:
            Dict[str, object] -- Contains result data of the current instance. Used keys are column names specified by the algorithm.
        """
        
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
            context {AlgTesterContext} -- Current application context.
            input_file {IO} -- The opened input file.
            parser {Parser} -- Currently used instances parser.
            algorithm {Algorithm} -- Currently tested algorithm.
        
        Returns:
            Dict[str, object] -- One parsed instance from the input file.
        """
        output = list()
        parsed_instance_data = parser.get_next_instance(input_file)
        
        click_options: Dict[str, object] = get_click_options(context, algorithm)
        
        output_file_name: str = parser.get_output_file_name(context, input_file, click_options)

        while parsed_instance_data is not None:
            parsed_instance_data["output_file_name"] = output_file_name
            parsed_instance_data["algorithm_name"] = algorithm.get_name()
            parsed_instance_data["algorithm"] = algorithm
            parsed_instance_data.update(context.extra_options)

            output.append(parsed_instance_data)

            parsed_instance_data = parser.get_next_instance(input_file)

        return output

    def run_tester_for_file(self, context: AlgTesterContext, input_file_path: str):
        """
        Compute results for the given input file.
        
        Arguments:
            context {AlgTesterContext} -- Current application context.
            input_file_path {str} -- Path to the input file to compute results for.
        """
        print(input_file_path)
        parser: Parser = plugins.get_parser(context.parser_name)
        communicators: List[Communicator] = get_communicators(context)
        
        print(f'Currently testing file \'{input_file_path.split("/")[-1]}\'. Started {time.strftime("%H:%M:%S %d.%m.")}')
        with open(input_file_path, "r") as input_file:
            for algorithm_name in context.algorithm_names:
                input_file.seek(0)
                algorithm: Algorithm = plugins.get_algorithm(algorithm_name)
                
                click_options = get_click_options(context, algorithm)
                output_file_name: str = parser.get_output_file_name(context, input_file, click_options)

                create_columns_description_file(context, algorithm)
                with open(f'{context.output_dir}/{output_file_name}', "w") as output_file:

                    for parsed_instance_data in self.get_parsed_instances_data(context, input_file, parser, algorithm):
                        solution = self.get_solution_for_instance(context, algorithm, parsed_instance_data)

                        parser.write_result_to_file(output_file, solution)
                        notify_communicators(context, communicators, output_file_name)

    def compute_results(self, context: AlgTesterContext, input_files: List[str]):
        """
        Parses instances from given input files, solve them using required algorithms and write results to the output file.
        
        Arguments:
            context {AlgTesterContext} -- Current application context.
            input_files {List[str]} -- Unsorted list of input file names.
        """

        for index, filename in enumerate(sorted(input_files)):
            if context.max_num is not None and index >= context.max_num:
                break

            input_file_path: str = f'{context.input_dir}/{filename}'
            self.run_tester_for_file(context, input_file_path)

class ConcurrentFilesRunner(Runner):
    """
    Processes multiple files concurrently. Instances in each file is processed sequentially.
    
    """
    _base_runner: BaseRunner = BaseRunner()

    def close_all_files(self, files_dict: Dict[str, IO]):
        for file in files_dict.values():
            if not file.closed:
                file.close()

    def get_base_instances(self, input_files: Dict[str, IO], parser: Parser) -> (Dict[str, object], IO):
        instances_remaining: bool = True
            
        while instances_remaining:
            instances_remaining = False
            
            for (filename, file) in input_files.items():
                # Get instances from accross all input files

                if file.closed:
                    continue

                instance = parser.get_next_instance(file)

                if instance is not None:
                    instances_remaining = True
                    yield (instance, file)
            
        print

    def write_result(self, context: AlgTesterContext, parser: Parser, output_files: Dict[str, IO], data: Dict[str, object]):
        output_filename: str = data["output_file_name"]

        if output_filename not in output_files:
            # Output file not yet opened
            output_files[output_filename] = open(f'{context.output_dir}/{output_filename}', "w")
        
        output_file: IO = output_files[output_filename]
        parser.write_result_to_file(output_file, data)

    def get_data_for_executor(self, context: AlgTesterContext, input_files_dict: Dict[str, IO], parser: Parser, algorithms: List[Algorithm]):
        for (instance_data, input_file) in self.get_base_instances(input_files_dict, parser):
            # Give all instances to the executor
            for alg in algorithms:
                click_options: Dict[str, object] = get_click_options(context, alg)
                output_filename: str = parser.get_output_file_name(context, input_file, click_options)

                instance_data["output_file_name"] = output_filename
                instance_data["algorithm_name"] = alg.get_name()
                instance_data["algorithm"] = alg
                yield (alg, instance_data)
                
        
    def compute_results(self, context: AlgTesterContext, input_files: List[str]):
        """
        Parses instances from given input files, solve them using required algorithms and write results to the output file.
        
        Arguments:
            context {AlgTesterContext} -- Current application context.
            input_files {List[str]} -- Unsorted list of input file names.
        """

        input_files_dict: Dict[str, IO] = dict()
        output_files_dict: Dict[str, IO] = dict()

        parser: Parser = plugins.get_parser(context.parser_name)
        communicators: List[Communicator] = get_communicators(context)
        algorithms: List[Algorithm] = [plugins.get_algorithm(alg_name) for alg_name in context.algorithm_names]

        for alg in algorithms:
            create_columns_description_file(context, alg)

        try:
            # Open all input files
            for index, filename in enumerate(sorted(input_files)):
                if context.max_num is not None and index >= context.max_num:
                    break
                
                input_files_dict[filename] = open(f'{context.input_dir}/{filename}', "r")

            with concurrent.futures.ProcessPoolExecutor() as executor:
                futures = list()
                for data in self.get_data_for_executor(context, input_files_dict, parser, algorithms):
                    # Give all instances to the executor
                    futures.append(executor.submit(self._base_runner.get_solution_for_instance, context, *data))

                for future in concurrent.futures.as_completed(futures):
                    # An instance is done, write it down and notify communicators
                    solution: Dict[str, object] = future.result()
                    self.write_result(context, parser, output_files_dict, solution)
                    # notify_communicators(context, communicators, output_file_name)
                    
        except Exception as e:
            print(f"Error occured: {e}")        
        finally:
            self.close_all_files(input_files_dict)
            self.close_all_files(output_files_dict)

class ConcurrentInstancesRunner(Runner):
    """
    Processes multiple instances of 1 file concurrently.
    
    """
    _base_runner: BaseRunner = BaseRunner()

    def compute_solution_for_file_and_algorithm(self, context: AlgTesterContext, input_file: IO, parser: Parser, algorithm: Algorithm, communicators: List[Communicator], executor: concurrent.futures.ProcessPoolExecutor):
        """
        Asynchronously gets results from multiple instances and writes them into the output file using the Parser.
        
        Arguments:
            context {AlgTesterContext} -- Current application context.
            input_file {IO} -- Opened input file with instances.
            parser {Parser} -- Currently used instances parser.
            algorithm {Algorithm} -- Currently tested algorithm.
            executor {concurrent.futures.ProcessPoolExecutor} -- [description]
        """
        
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
                notify_communicators(context, communicators, output_file_name)

    def run_tester_for_file(self, context: AlgTesterContext, input_file_path: str, executor: concurrent.futures.ProcessPoolExecutor):
        """
        Run all algorithms for the selected file.
        
        Arguments:
            context {AlgTesterContext} -- Current application context.
            input_file_path {str} -- String path to the input file
            executor {concurrent.futures.ProcessPoolExecutor} -- [description]
        """
        
        parser: Parser = plugins.get_parser(context.parser_name)
        communicators: List[Communicator] = get_communicators(context)
        
        print(f'Currently testing file \'{input_file_path.split("/")[-1]}\'. Started {time.strftime("%H:%M:%S %d.%m.")}')
        with open(input_file_path, "r") as input_file:
            for algorithm_name in context.algorithm_names:
                algorithm: Algorithm = plugins.get_algorithm(algorithm_name)
                
                self.compute_solution_for_file_and_algorithm(context, input_file, parser, algorithm, communicators, executor)

    def compute_results(self, context: AlgTesterContext, input_files: List[str]):
        """
        Parses instances from given input files, solve them using required algorithms and write results to the output file.
        
        Arguments:
            context {AlgTesterContext} -- Current application context.
            input_files {List[str]} -- Unsorted list of input file names.
        """
        with concurrent.futures.ProcessPoolExecutor(initializer=init_globals, initargs=(context.num_of_instances_done,)) as executor:

            for index, filename in enumerate(sorted(input_files)):
                if context.max_num is not None and index >= context.max_num:
                    break

                input_file_path: str = f'{context.input_dir}/{filename}'
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