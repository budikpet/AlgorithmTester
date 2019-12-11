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

    def get_column_descriptions(self, show_time: bool = True):
        output = [
            "id",
            "item_count",
            "maximum_sum",
            "algorithm",
            "|",
            "items_in_bag"
        ]

        if show_time:
            # time counted as real time
            output.insert(output.index("|"), "time[ms]")
        else:
            # time counted as number of configurations
            output.insert(output.index("|"), "time[#configs]")

        return output

    def get_name(self) -> str:
        pass
    
    def perform_algorithm(self, parsed_data: Dict[str, object]) -> Dict[str, object]:
        pass