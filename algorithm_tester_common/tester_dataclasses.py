from dataclasses import dataclass, field
from typing import List, Tuple, Dict, IO
from enum import Enum
import re

class AlgTesterContext():
    """
    Contains all options and arguments given to the application.
    """

    def __init__(self, algorithms: List[str], parser: str, concurrency_runner: str, communicators: List[str], check_time: bool, time_retries: int, max_num: int, extra_options: Dict[str, object], input_dir, output_dir):
        self.algorithm_names: List[str] = algorithms
        self.parser_name: str = parser
        self.communicator_names: List[str] = communicators
        self.concurrency_runner_name: str = concurrency_runner
        self.check_time: bool = check_time
        self.time_retries: int = time_retries
        self.max_num: int = max_num
        self.extra_options: Dict[str, object] = extra_options
        self.input_dir: str = input_dir
        self.output_dir: str = output_dir
        
        self.start_time = None
        self.num_of_instances = None
        self.num_of_instances_done = 0

        if self.extra_options is None:
            self.extra_options = dict()

    def get_options(self) -> Dict[str, object]:
        options = {
            "algorithm_names": self.algorithm_names,
            "parser_name": self.parser_name,
            "communicator_names": self.communicator_names,
            "check_time": self.check_time,
            "time_retries": self.time_retries,
            "max_num": self.max_num,
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
        
        Args:
            parsed_data (Dict[str, object]): Instance data from a parser.
        
        Returns:
            Dict[str, object]: Instance result data. Which values should be part of the output file is determined by the output of get_columns method.
        """
        pass

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