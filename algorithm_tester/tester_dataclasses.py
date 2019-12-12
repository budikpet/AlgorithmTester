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

class TesterContext():

    def __init__(self, algorithm):
        self.algorithm = algorithm

    def perform_algorithm(self, parsed_data: Dict[str, object]) -> Dict[str, object]:
        return self.algorithm.perform_algorithm(parsed_data)

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

    def get_name(self) -> str:
        pass

    def get_output_file_name(click_args: Dict[str, object]) -> str:
        pass