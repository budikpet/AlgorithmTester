from dataclasses import dataclass, field
from typing import List, Tuple, Dict
from enum import Enum
import re
import numpy as np

base_columns: List[str] = [
        "id",
        "item_count",
        "algorithm_name",
        "found_value",
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