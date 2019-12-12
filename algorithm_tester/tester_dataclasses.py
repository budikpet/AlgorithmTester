from dataclasses import dataclass, field
from typing import List, Tuple, Dict
from enum import Enum
import re
import numpy as np

class AnalysisFile:

    def __init__(self, filename: str, full_path: str):
        parts = filename.replace(".dat", "").split("_")
        # self.num_of_items = int(re.findall("[0-9]+", parts[0])[0])
        self.dataset = parts[0]
        self.instance_info = parts[1]
        self.algorithm = parts[3]
        
        if len(parts) > 4:
            self.relative_mistake = float(parts[3].replace(",", "."))
        else:
            self.relative_mistake = float(-1)

        self.full_path = full_path

@dataclass
class DynamicClickOption():
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

    def required_click_params(self) -> List[DynamicClickOption]:
        pass

    def get_additional_columns(self, show_time: bool = True) -> List[str]:
        output = [
            "maximum_sum",
            "elapsed_configs",
            "items_in_bag"
        ]

        return output

    def get_name(self) -> str:
        pass
    
    def perform_algorithm(self, parsed_data: Dict[str, object]) -> Dict[str, object]:
        pass

class Parser(object):

    def set_input_file(self, input_file):
        self.input_file = input_file

    def reload_input_file(self):
        self.input_file.seek(0)

    def get_name(self) -> str:
        pass

    def get_output_file_name(self, click_args: Dict[str, object]) -> str:
        pass

    def get_next_instance(self) -> Dict[str, object]:
        pass

class TesterContext():

    def __init__(self, algorithms: List[str], parser: str, communicators: List[str], check_time: bool, time_retries: int, max_num: int, other_options: Dict[str, object], input_dir, output_dir):
        self.algorithm_names: List[str] = algorithms
        self.parser_name: str = parser
        self.communicator_names: List[str] = communicators
        self.check_time: bool = check_time
        self.time_retries: int = time_retries
        self.max_num: int = max_num
        self.other_options: Dict[str, object] = other_options
        self.input_dir: str = input_dir
        self.output_dir: str = output_dir

        if self.other_options is None:
            self.other_options = dict()

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

        options.update(self.other_options)

        return options