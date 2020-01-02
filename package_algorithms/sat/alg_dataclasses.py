from dataclasses import dataclass, field
from typing import List, Tuple, Dict
from enum import Enum
import re
import numpy as np
from algorithm_tester_common.tester_dataclasses import AlgTesterContext

class TaskSAT:
    
    def __init__(self, parsed_data: Dict[str, object]):
        self.num_of_vars: int = parsed_data.get("num_of_vars")
        self.num_of_clauses: int = parsed_data.get("num_of_clauses")
        self.clauses: List[List[int]] = parsed_data.get("clauses")
        self.algorithm: str = parsed_data.get("algorithm_name")
        self.weights: List[int] = parsed_data.get("weights")

# class Solution:
#     id: int
#     count: int
#     algorithm: str
#     max_value: int
#     relative_mistake: float = None
#     # Tuple of 1's and 0's
#     things: Tuple[int] = None

#     # Elapsed time in millis
#     elapsed_time: float = None
#     # Elapsed time in number of configurations
#     elapsed_configs: int = None

#     def __init__(self, task: TaskKnapsackProblem, max_value: int, things, elapsed_configs: int = None, elapsed_time: float = None, relative_mistake: float = None):
#         self.things = things
#         self.max_value = max_value
#         self.elapsed_configs = elapsed_configs
#         self.elapsed_time = elapsed_time
#         self.relative_mistake = relative_mistake
#         self.id = task.id
#         self.count = task.count
#         self.algorithm = task.algorithm

#     def output_str(self) -> str:
#         output = f'{abs(self.id)} {self.count} {self.max_value} {self.algorithm}'

#         if self.elapsed_time is not None or self.elapsed_configs is not None:
#             if self.elapsed_time is not None:
#                 output = f'{output} {self.elapsed_time}'
#             else:
#                 output = f'{output} {self.elapsed_configs}'

#         if self.relative_mistake is not None:
#             output = f'{output} {self.relative_mistake}'

#         return f'{output} | {" ".join(map(str, self.things))}'

# class SolutionSA():

#     def __init__(self, solution: np.ndarray, sum_cost: int, sum_weight: int):
#         self.solution: np.ndarray = solution
#         self.sum_cost: int = sum_cost
#         self.sum_weight: int = sum_weight
    
#     def __getitem__(self, key):
#         return self.solution[key]
    
#     def __setitem__(self, key, value):
#         self.solution[key] = value

#     def copy(self, other):
#         np.copyto(self.solution, other.solution)
#         self.sum_cost = other.sum_cost
#         self.sum_weight = other.sum_weight