from dataclasses import dataclass, field
from typing import List, Tuple, Dict
from enum import Enum
import re
import numpy as np
from algorithm_tester_common.tester_dataclasses import AlgTesterContext

base_columns: List[str] = [
        "id",
        "item_count",
        "found_value",
        "algorithm_name",
        "elapsed_configs",
        "elapsed_time",
        "things"
    ]

@dataclass
class Thing:
    position: int
    weight: int
    cost: int

class TaskKnapsackProblem:
    
    def __init__(self, parsed_data: Dict[str, object]):
        self.id: int = parsed_data.get("id")
        self.count: int = parsed_data.get("item_count")
        self.capacity: int = parsed_data.get("capacity")
        self.algorithm: str = parsed_data.get("algorithm_name")
        # None if not used
        self.relative_mistake: float = parsed_data.get("relative_mistake")
        self.things: List[Thing] = [Thing(pos, weight, cost) for pos, weight, cost in parsed_data.get("things")]

class TaskSA(TaskKnapsackProblem):
    
    def __init__(self, context: AlgTesterContext, parsed_data: Dict[str, object]):
        super().__init__(parsed_data)
        self.init_temp: float = context.extra_options.get("init_temperature")
        self.cooling_coefficient: float = context.extra_options.get("cooling")
        self.min_temp: float = context.extra_options.get("min_temperature")
        self.cycles: int = context.extra_options.get("cycles")
        self.output_file_name: str = parsed_data.get("output_file_name")
        self.output_dir: str = context.output_dir
        
        self.evo_filepath = None
        if context.extra_options.get("create_evo_file") is not None:
            if context.extra_options.get("create_evo_file") == True:
                self.evo_filepath = f'{self.output_dir}/{self.output_file_name.replace(".dat", ".evo")}'

class Solution:
    id: int
    count: int
    algorithm: str
    max_value: int
    relative_mistake: float = None
    # Tuple of 1's and 0's
    things: Tuple[int] = None

    # Elapsed time in millis
    elapsed_time: float = None
    # Elapsed time in number of configurations
    elapsed_configs: int = None

    def __init__(self, task: TaskKnapsackProblem, max_value: int, things, elapsed_configs: int = None, elapsed_time: float = None, relative_mistake: float = None):
        self.things = things
        self.max_value = max_value
        self.elapsed_configs = elapsed_configs
        self.elapsed_time = elapsed_time
        self.relative_mistake = relative_mistake
        self.id = task.id
        self.count = task.count
        self.algorithm = task.algorithm

    def output_str(self) -> str:
        output = f'{abs(self.id)} {self.count} {self.max_value} {self.algorithm}'

        if self.elapsed_time is not None or self.elapsed_configs is not None:
            if self.elapsed_time is not None:
                output = f'{output} {self.elapsed_time}'
            else:
                output = f'{output} {self.elapsed_configs}'

        if self.relative_mistake is not None:
            output = f'{output} {self.relative_mistake}'

        return f'{output} | {" ".join(map(str, self.things))}'

class SolutionSA():

    def __init__(self, solution: np.ndarray, sum_cost: int, sum_weight: int):
        self.solution: np.ndarray = solution
        self.sum_cost: int = sum_cost
        self.sum_weight: int = sum_weight
    
    def __getitem__(self, key):
        return self.solution[key]
    
    def __setitem__(self, key, value):
        self.solution[key] = value

    def copy(self, other):
        np.copyto(self.solution, other.solution)
        self.sum_cost = other.sum_cost
        self.sum_weight = other.sum_weight

@dataclass
class ConfigCounter:
    value: int

@dataclass
class RecursiveResult:
    remaining_capacity: int
    max_value: int
    things: np.ndarray

    def new_solution(self, thing: Thing = None):        
        if thing is not None:
            things = np.copy(self.things)
            things[thing.position] = 1
            return RecursiveResult(self.remaining_capacity - thing.weight, self.max_value + thing.cost, things)
        else:
            return RecursiveResult(self.remaining_capacity, self.max_value, np.copy(self.things))