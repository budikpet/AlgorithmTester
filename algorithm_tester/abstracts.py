from enum import Enum
from typing import List, Dict
import numpy as np
from algorithm_tester.tester_dataclasses import DynamicClickOption

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

    def get_output_file_name(solution_data: Dict[str, object]) -> str:
        pass