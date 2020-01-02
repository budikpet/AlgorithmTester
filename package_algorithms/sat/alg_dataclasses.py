from dataclasses import dataclass, field
from typing import List, Tuple, Dict
from enum import Enum
import re
import numpy as np
from algorithm_tester_common.tester_dataclasses import AlgTesterContext

class TaskSAT:
    
    def __init__(self, context: AlgTesterContext, parsed_data: Dict[str, object]):
        self.num_of_vars: int = parsed_data.get("num_of_vars")
        self.num_of_clauses: int = parsed_data.get("num_of_clauses")
        self.clauses: np.ndarray = parsed_data.get("clauses")
        self.algorithm: str = parsed_data.get("algorithm_name")
        self.weights: np.ndarray = parsed_data.get("weights")
        self.all_weights_sum: int = sum(self.weights)

        self.cooling: float = context.extra_options["cooling"]
        self.cycles: float = context.extra_options["cycles"]
        self.init_temp: float = context.extra_options["init_temperature"]
        self.min_temp: float = context.extra_options["min_temperature"]

class SolutionSA():

    def __init__(self, solution: np.ndarray, sum_value: int, is_valid: bool):
        self.solution: np.ndarray = solution    # 01 array, length of number of variables
        self.sum_value: int = sum_value
        self.is_valid: bool = is_valid

    def copy(self, other):
        np.copyto(self.solution, other.solution)
        self.sum_value = other.sum_value
        self.is_valid = other.is_valid