from dataclasses import dataclass, field
from typing import List, Tuple, Dict
from enum import Enum
import re
import numpy as np
from algorithm_tester_common.tester_dataclasses import AlgTesterContext

base_columns: List[str] = [
    "output_filename",
    "found_value",
    "vars_output",      # numbers [1..number_of_vars], negative if result is negated
    "num_of_vars",
    "num_of_clauses",
    "algorithm_name",
    "init_temperature",
    "min_temperature",
    "cooling",
    "cycles",
    "is_valid",
    "num_of_satisfied_clauses",
    "retry_count",
    "elapsed_configs",
    "elapsed_time"
]

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
        self.max_retry_attempts: int = context.extra_options["max_retry_attempts"]

class SolutionSA():
    """
    Arguments:
        solution (np.ndarray): 0,1 array length of number of variables. Settings of all variables.
        invalid_literals_per_var (np.ndarray): Int array length of number of variables. i'th position has a number which means in how many clauses is the i'th variable false with current settings.
        sum_weight (int): Sum of weights of all variables that are set to 1.
        num_of_satisfied_clauses (int): How many whole clauses are true with current settings.
        is_valid (bool): True if all clauses are satisfied.
    """

    def __init__(self, solution: np.ndarray, sum_weight: int):
        self.solution: np.ndarray = solution    # 01 array, length of number of variables
        self.invalid_literals_per_var: np.ndarray = np.zeros(self.solution.shape, dtype=int)
        self.sum_weight: int = sum_weight
        self.num_of_satisfied_clauses = 0
        self.is_valid: bool = False

    def copy(self, other):
        np.copyto(self.solution, other.solution)
        np.copyto(self.invalid_literals_per_var, other.invalid_literals_per_var)
        self.sum_weight = other.sum_weight
        self.num_of_satisfied_clauses = other.num_of_satisfied_clauses
        self.is_valid = other.is_valid