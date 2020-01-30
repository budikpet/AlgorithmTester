import os
import shutil
from dataclasses import dataclass
from typing import List, Tuple, Dict, IO
from enum import Enum
import algorithm_tester.helpers as helpers

class AlgTesterContext():
    """
    Contains all options and arguments given to the application.
    """

    def __init__(self, algorithms: List[str], parser: str, concurrency_runner: str, communicators: List[str], check_time: bool, time_retries: int, max_num: int, is_forced: bool, extra_options: Dict[str, object], min_communicator_delay: float, input_dir, output_dir):
        self.algorithm_names: List[str] = algorithms
        self.parser_name: str = parser
        self.communicator_names: List[str] = communicators
        self.concurrency_runner_name: str = concurrency_runner
        self.check_time: bool = check_time
        self.time_retries: int = time_retries
        self.max_files_to_check: int = max_num
        self.is_forced: bool = is_forced
        self.extra_options: Dict[str, object] = extra_options
        self.input_dir: str = input_dir
        self.output_dir: str = output_dir
        self.min_time_between_communications: float = min_communicator_delay
        
        self.start_time: int = None
        self.num_of_instances: int = None

        if self.extra_options is None:
            self.extra_options = dict()

    def get_options(self) -> Dict[str, object]:
        options = {
            "algorithm_names": self.algorithm_names,
            "parser_name": self.parser_name,
            "communicator_names": self.communicator_names,
            "check_time": self.check_time,
            "time_retries": self.time_retries,
            "max_files_to_check": self.max_files_to_check,
            "input_dir": self.input_dir,
            "output_dir": self.output_dir
        }

        options.update(self.extra_options)

        return options

@dataclass
class DynamicClickOption():
    """
    Class that represents extra option that is required by an Algorithm subclass.

    Args:
        name (str): Name of the argument (dict key) for the option.
        data_type (type): Click CLI type of the option value.
        short_opt (str): Short option name (e. g. -f).
        long_opt (str): Long option name (e. g. --force).
        required (bool): True if the option must be provided.
        doc_help (str): A string that should be part of the documentation.
    
    """

    name: str
    data_type: type
    short_opt: str
    long_opt: str = None
    required: bool = False
    doc_help: str = None

    def __key(self):
        return (self.name)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, DynamicClickOption):
            return self.__key() == other.__key()
        return NotImplemented

class InstancesLogger():
    """
    Class that persists created instances in a log that can be later used to resume computation without deleting old results.
    """

    def __init__(self, output_dir: str, is_forced: bool):
        self._output_dir: str = output_dir
        self._loaded_instances: Dict[str, List[str]] = list()
        self._instance_log: IO = None
        self._instances_log_filename: str = ".instances_log.dat"

        if is_forced:
            # Remove instance files if forced = True
            shutil.rmtree(output_dir)
            helpers.create_path(output_dir)
        else:
            # Read already created instances from log
            self.load_instances()

    def load_instances(self):
        """
        Loads identifiers of all done instances.
        """
        filepath: str = f'{self._output_dir}/{self._instances_log_filename}'
        if not os.path.isfile(filepath):
            return
        
        with open(filepath, "r") as instances_log:
            instance_data: str = input_file.readline()

            while instance_data is not None or instance_data != "":
                split = instance_data.split(" ")
                algorithm_name: str = split[0]
                
                if algorithm_name not in self._loaded_instances:
                    self._loaded_instances[algorithm_name] = list()
                
                self._loaded_instances[algorithm_name].append(instance_data)
    
    def get_num_of_instances(self) -> int:
        return len(self._loaded_instances)

    def write_instance_to_log(self, instance_identifier: str):
        if self._instance_log is None:
            self._instance_log = open(f'{self._output_dir}/{self._instances_log_filename}', 'w+')
        
        self._instance_log.write(f'{instance_identifier}\n')
    
    def close_log(self):
        if self._instance_log is not None and not self._instance_log.closed():
            self._instance_log.close()

class Algorithm(object):
    """
    Interface for algorithm plugins.
    
    """

    def required_click_params(self) -> List[DynamicClickOption]:
        """
        
        Returns:
            List[DynamicClickOption]: List of possible DynamicOptions for the algorithm.
        """
        pass

    def get_columns(self) -> List[str]:
        """
        
        
        Returns:
            List[str]: List of column names that should be part of the output file. These column names need to correspond to dictionary keys of perform_algorithm method.
        """
        pass

    def get_name(self) -> str:
        """
        
        Returns:
            str: Name of this algorithm that is used to identify it.
        """
        pass
    
    def perform_algorithm(self, context: AlgTesterContext, parsed_data: Dict[str, object]) -> Dict[str, object]:
        """
        Main method of the class. Receives instance data from a parser and creates results.
        
        Arguments:
            context {AlgTesterContext} -- Used context.
            parsed_data {Dict[str, object]} -- Input instance data
        
        Returns:
            Dict[str, object] -- Instance result data. Which values should be part of the output file is determined by the output of get_columns method.
        """
        
        pass

   
    def _run_perform_algorithm_func(self, context: AlgTesterContext, parsed_data: Dict[str, object]) -> Dict[str, object]:
        """
        Run the perform_algorithm method. 
        Makes sure that important input data is still present in the output. This data is used further in the programme.
        
        Arguments:
            context {AlgTesterContext} -- Used context.
            parsed_data {Dict[str, object]} -- Input instance data
        
        Returns:
            Dict[str, object] -- Instance result data. Which values should be part of the output file is determined by the output of get_columns method.
        """
        important_data = dict()
        important_keys: List[str] = ["output_filename", "algorithm_name", "algorithm"]
        for key in important_keys:
            important_data[key] = parsed_data.get(key)

        output_data = self.perform_algorithm(context, parsed_data)

        # Put data back if it doesn't exist in the output
        for key in important_keys:
            if key not in output_data:
                output_data[key] = important_data[key]

        return output_data

class Parser(object):

    def get_name(self) -> str:
        """
        
        Returns:
            str: Name of this parser that is used to identify it.
        """
        pass

    def get_output_file_name(self, context: AlgTesterContext, input_file: IO, click_args: Dict[str, object]) -> str:
        """
        Construct name of an output file using provided data.
        
        Args:
            click_args (Dict[str, object]): Options that were given to the script.
        
        Returns:
            str: Name of the output file.
        """
        pass

    def get_num_of_instances(self, context: AlgTesterContext, input_file: IO) -> int:
        """
        Returns number of instances contained in that particular file.
        
        Arguments:
            context {AlgTesterContext} -- [description]
            input_file {IO} -- Instances file.
        
        Returns:
            int -- Number of instances contained in the input file.
        """
        pass

    def get_next_instance(self, input_file: IO) -> Dict[str, object]:
        """
        Parses next instance from an input file and returns it.
        
        Returns:
            Dict[str, object]: Instance data (or None if no data remains).
        """
        pass

    def write_result_to_file(self, output_file: IO, data: Dict[str, object]):
        """
        Write result data to an output file.
        
        Args:
            output_file: Opened output file.
            data (Dict[str, object]): Result data from an algorithm and options that were given to the script.
        """
        pass

class Communicator:

    def get_name(self) -> str:
        """
        
        Returns:
            str: Name of this communicator that is used to identify it.
        """
        pass
        
    def notify_instance_computed(self, context: AlgTesterContext, last_solution: Dict[str, object], num_of_instances_done: int, num_of_instances_failed: int):
        """
        The communicator is notified when an instance is computed.
        
        Arguments:
            context {AlgTesterContext} -- [description]
            output_filename {str} -- [description]
        """
        pass