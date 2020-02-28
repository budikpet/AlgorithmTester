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

    def notify_communicators(self, context: AlgTesterContext, communicators: List[Communicator], solution: Dict[str, object], notification_vars: Dict[str, object], forced: bool = False) -> bool:
        """
        Notifies all Communicators that a instance was computed if enough time has passed since the last notification.

        Updates last_communication_time and instances_done variables.
        
        Arguments:
            context {AlgTesterContext} -- Used context.
            communicators {List[Communicator]} -- All available communicators.
            solution {Dict[str, object]} -- All solution data.
            notification_vars {Dict[str, object]} -- Contains last_communication_time and instances_done.

        Returns:
            Bool -- True if communicators were notified, False if not
        """
        curr_time: float = curr_time_millis()

        last_communication_time = notification_vars["last_comm_time"]

        if ((curr_time - last_communication_time) >= context.min_time_between_communications) or forced:
            # Notify communicators
            notification_vars["last_comm_time"] = curr_time

            for communicator in communicators:
                communicator.notify_instance_computed(context, solution, notification_vars["instances_done"], notification_vars["instances_failed"])

            return True

        return False

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
            t = timeit.Timer(lambda: algorithm._run_perform_algorithm_func(context, parsed_instance_data))
            elapsed_time, solution = t.timeit(number=context.time_retries)
            solution["elapsed_time"] = round((elapsed_time*1000)/context.time_retries, 10)   # Store in millis
        else:
            solution = algorithm._run_perform_algorithm_func(context, parsed_instance_data)

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
        
        output_filename: str = parser.get_output_file_name(context, input_file, click_options)

        while parsed_instance_data is not None:
            parsed_instance_data["output_filename"] = output_filename
            parsed_instance_data["algorithm_name"] = algorithm.get_name()
            parsed_instance_data["algorithm"] = algorithm
            parsed_instance_data.update(context.extra_options)

            output.append(parsed_instance_data)

            parsed_instance_data = parser.get_next_instance(input_file)

        return output

    def run_tester_for_file_algorithm(self, context: AlgTesterContext, parser: Parser, algorithm: Algorithm, communicators: Communicator, input_file: IO, notification_vars: Dict[str, object]):
        """
        Opens an output file and writes solutions into it using the specified algorithm.
        
        Arguments:
            context {AlgTesterContext} -- Used context.
            parser {Parser} -- Used parser.
            algorithm {Algorithm} -- Used algorithm.
            communicators {Communicator} -- Used communicators.
            input_file {IO} -- Opened input file.
            notification_vars {Dict[str, object]} -- Used notification variables.
        """
        click_options = get_click_options(context, algorithm)
        output_filename: str = parser.get_output_file_name(context, input_file, click_options)

        with open(f'{context.output_dir}/{output_filename}', "w+") as output_file:
            for parsed_instance_data in self.get_parsed_instances_data(context, input_file, parser, algorithm):
                # Use solution only if no exception was raised
                try:
                    solution = self.get_solution_for_instance(context, algorithm, parsed_instance_data)
                except Exception as e:
                    print(f'Algorithm {algorithm.get_name()}. Exception occured: {e}')
                    notification_vars["instances_failed"] += 1
                else:
                    parser.write_result_to_file(output_file, solution)
                    notification_vars["instances_done"] += 1
                    self.notify_communicators(context, communicators, solution, notification_vars)

    def run_tester_for_file(self, context: AlgTesterContext, input_file_path: str, notification_vars: Dict[str, object]):
        """
        Compute results for the given input file.
        
        Arguments:
            context {AlgTesterContext} -- Current application context.
            input_file_path {str} -- Path to the input file to compute results for.
        """
        print(input_file_path)
        parser: Parser = plugins.get_parser(context.parser_name)
        communicators: List[Communicator] = get_communicators(context)
        solution = dict()
        
        print(f'Currently testing file \'{input_file_path.split("/")[-1]}\'. Started {time.strftime("%H:%M:%S %d.%m.")}')
        with open(input_file_path, "r") as input_file:
            for algorithm_name in context.algorithm_names:
                input_file.seek(0)
                algorithm: Algorithm = plugins.get_algorithm(algorithm_name)

                create_columns_description_file(context, algorithm)
                self.run_tester_for_file_algorithm(context, parser, algorithm, communicators, input_file, notification_vars)
        
        self.notify_communicators(context, communicators, solution, notification_vars, forced=True)

    def compute_results(self, context: AlgTesterContext, input_files: List[str]):
        """
        Parses instances from given input files, solve them using required algorithms and write results to the output file.
        
        Arguments:
            context {AlgTesterContext} -- Current application context.
            input_files {List[str]} -- Unsorted list of input file names.
        """

        notification_vars: Dict[str, object] = {"instances_done": 0, "last_comm_time": 0.0, "instances_failed": 0}
        for index, filename in enumerate(sorted(input_files)):
            if context.max_files_to_check is not None and index >= context.max_files_to_check:
                break

            input_file_path: str = f'{context.input_dir}/{filename}'
            self.run_tester_for_file(context, input_file_path, notification_vars)

class ConcurrentFilesRunner(Runner):
    """
    Processes multiple files concurrently.

    Technically reads first instances of all files and stores them for multiprocessing. 
    Then reads second instances of all files and stores them for multiprocessing. 
    This repeats until no new instances are left in any input file.
    
    """
    _base_runner: BaseRunner = BaseRunner()

    def close_all_files(self, files_dict: Dict[str, IO]):
        """
        Close all unclosed files.
        
        Arguments:
            files_dict {Dict[str, IO]} -- Opened and closed files.
        """
        for file in files_dict.values():
            if not file.closed:
                file.close()

    def get_base_instances(self, input_files: Dict[str, IO], parser: Parser) -> (Dict[str, object], IO):
        """
        Reads instance data directly from all input files.
        
        Arguments:
            input_files {Dict[str, IO]} -- All opened input files.
            parser {Parser} -- Used parser.
        
        Yields:
            (Dict[str, object], IO) -- Opened input file and instance data of one of its instances.
        """
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

    def get_data_for_executor(self, context: AlgTesterContext, input_files_dict: Dict[str, IO], parser: Parser, algorithms: List[Algorithm]):
        """
        Fully prepares instance data that is to be used for an algorithm.
        
        Arguments:
            context {AlgTesterContext} -- Used context.
            input_files_dict {Dict[str, IO]} -- All currently opened input files.
            parser {Parser} -- Used parser.
            algorithms {List[Algorithm]} -- List of all used algorithms.
        
        Yields:
            (Algorithm, Dict[str, object]) -- Used algorithm and full instance data.
        """
        for (instance_data, input_file) in self.get_base_instances(input_files_dict, parser):
            # Give all instances to the executor
            for alg in algorithms:
                click_options: Dict[str, object] = get_click_options(context, alg)
                output_filename: str = parser.get_output_file_name(context, input_file, click_options)

                instance_data["output_filename"] = output_filename
                instance_data["algorithm_name"] = alg.get_name()
                instance_data["algorithm"] = alg
                yield (alg, instance_data)

    def write_result(self, context: AlgTesterContext, parser: Parser, output_files: Dict[str, IO], data: Dict[str, object]):
        """
        Writes results into an appropriate output file.
        
        Arguments:
            context {AlgTesterContext} -- Used context.
            parser {Parser} -- Used parser.
            output_files {Dict[str, IO]} -- Dictionary of all currently opened output files.
            data {Dict[str, object]} -- Computation results of an instance.
        """
        output_filename: str = data["output_filename"]

        if output_filename not in output_files:
            # Output file not yet opened
            output_files[output_filename] = open(f'{context.output_dir}/{output_filename}', "w+")
        
        output_file: IO = output_files[output_filename]
        parser.write_result_to_file(output_file, data)

    def run_tester_for_data(self, context: AlgTesterContext, algorithms: List[Algorithm], parser: Parser, communicators: List[Communicator], input_files_dict: Dict[str, IO], output_files_dict: Dict[str, IO]):
        """
        Parses instances from given input files, solve them using required algorithms and write results to the output file.
        
        Arguments:
            context {AlgTesterContext} -- Used context.
            algorithms {List[Algorithm]} -- Used algorithms.
            parser {Parser} -- Used parser.
            communicators {List[Communicator]} -- Used communicators.
            input_files_dict {Dict[str, IO]} -- Opened input files.
            output_files_dict {Dict[str, IO]} -- A dictionary for all output files to be opened.
        """
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = list()
            for data in self.get_data_for_executor(context, input_files_dict, parser, algorithms):
                # Give all instances to the executor
                futures.append(executor.submit(self._base_runner.get_solution_for_instance, context, *data))

            notification_vars: Dict[str, object] = {"instances_done": 0, "last_comm_time": 0.0, "instances_failed": 0}
            for future in concurrent.futures.as_completed(futures):
                # An instance is done, write it down and notify communicators
                try:
                    solution: Dict[str, object] = future.result()
                except Exception as e:
                    print(f'Exception occured: {e}')
                    notification_vars["instances_failed"] += 1
                else:
                    self.write_result(context, parser, output_files_dict, solution)
                    notification_vars["instances_done"] += 1
                    self._base_runner.notify_communicators(context, communicators, solution, notification_vars)

            self._base_runner.notify_communicators(context, communicators, solution, notification_vars, forced=True)

            # Close all input files
            self.close_all_files(input_files_dict)
        
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
                if context.max_files_to_check is not None and index >= context.max_files_to_check:
                    break
                
                input_files_dict[filename] = open(f'{context.input_dir}/{filename}', "r")

            self.run_tester_for_data(context, algorithms, parser, communicators, input_files_dict, output_files_dict)

        except Exception as e:
            print(f"Error occured: {e}")        
        finally:
            # Make sure all input and output files are closed.
            self.close_all_files(input_files_dict)
            self.close_all_files(output_files_dict)

class ConcurrentInstancesRunner(Runner):
    """
    Processes multiple instances of 1 file concurrently.
    
    """
    _base_runner: BaseRunner = BaseRunner()

    def compute_solution_for_file_and_algorithm(self, context: AlgTesterContext, input_file: IO, parser: Parser, algorithm: Algorithm, communicators: List[Communicator], notification_vars: Dict[str, object], executor: concurrent.futures.ProcessPoolExecutor):
        """
        Asynchronously gets results from multiple instances and writes them into the output file using the Parser.
        
        Arguments:
            context {AlgTesterContext} -- Current application context.
            input_file {IO} -- Opened input file with instances.
            parser {Parser} -- Currently used instances parser.
            algorithm {Algorithm} -- Currently tested algorithm.
            notification_vars {Dict[str, object]} -- Notification variables
            executor {concurrent.futures.ProcessPoolExecutor} -- [description]
        """
        
        click_options = get_click_options(context, algorithm)
        output_filename: str = parser.get_output_file_name(context, input_file, click_options)
        solution: Dict[str, object] = dict()

        create_columns_description_file(context, algorithm)
        with open(f'{context.output_dir}/{output_filename}', "w+") as output_file:
            it = self._base_runner.get_parsed_instances_data(context, input_file, parser, algorithm)
            futures = [executor.submit(self._base_runner.get_solution_for_instance, context, algorithm, instance) for instance in it]

            for future in concurrent.futures.as_completed(futures):
                # Write results and notify communicators                
                try:
                    solution: Dict[str, object] = future.result()
                except Exception as e:
                    print(f'Exception occured: {e}')
                    notification_vars["instances_failed"] += 1
                else:
                    parser.write_result_to_file(output_file, solution)
                    notification_vars["instances_done"] += 1
                    self._base_runner.notify_communicators(context, communicators, solution, notification_vars)
        
        self._base_runner.notify_communicators(context, communicators, solution, notification_vars, forced=True)

    def run_tester_for_file(self, context: AlgTesterContext, input_file_path: str, notification_vars: Dict[str, object], executor: concurrent.futures.ProcessPoolExecutor):
        """
        Run all algorithms for the selected file.
        
        Arguments:
            context {AlgTesterContext} -- Current application context.
            input_file_path {str} -- String path to the input file
            notification_vars {Dict[str, object]} -- Notification variables
            executor {concurrent.futures.ProcessPoolExecutor} -- [description]
        """
        
        parser: Parser = plugins.get_parser(context.parser_name)
        communicators: List[Communicator] = get_communicators(context)
        
        print(f'Currently testing file \'{input_file_path.split("/")[-1]}\'. Started {time.strftime("%H:%M:%S %d.%m.")}')
        with open(input_file_path, "r") as input_file:
            for algorithm_name in context.algorithm_names:
                algorithm: Algorithm = plugins.get_algorithm(algorithm_name)
                
                self.compute_solution_for_file_and_algorithm(context, input_file, parser, algorithm, communicators, notification_vars, executor)

    def compute_results(self, context: AlgTesterContext, input_files: List[str]):
        """
        Parses instances from given input files, solve them using required algorithms and write results to the output file.
        
        Arguments:
            context {AlgTesterContext} -- Current application context.
            input_files {List[str]} -- Unsorted list of input file names.
        """
        with concurrent.futures.ProcessPoolExecutor() as executor:

            notification_vars: Dict[str, object] = {"instances_done": 0, "last_comm_time": 0.0, "instances_failed": 0}
            for index, filename in enumerate(sorted(input_files)):
                if context.max_files_to_check is not None and index >= context.max_files_to_check:
                    break

                input_file_path: str = f'{context.input_dir}/{filename}'
                self.run_tester_for_file(context, input_file_path, notification_vars, executor)

class Runners(Enum):
    """
    Contains references to all Concurrency runners available.
    
    Arguments:
        Enum {Runner} -- A concurrency runner.
    """
    BASE = BaseRunner()
    FILES = ConcurrentFilesRunner()
    INSTANCES = ConcurrentInstancesRunner()