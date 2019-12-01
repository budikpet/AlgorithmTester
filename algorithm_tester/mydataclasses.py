from dataclasses import dataclass, field
from typing import List, Tuple
from enum import Enum
import re
import numpy as np

@dataclass
class Thing:
    position: int
    weight: int
    cost: int

@dataclass
class Task:
    id: int
    count: int
    capacity: int
    strategy: str
    # None if not used
    relative_mistake: float
    things: List[Thing] = field(default_factory=list)

class AnalysisFile:

    def __init__(self, filename: str, full_path: str):
        parts = filename.replace(".dat", "").split("_")
        # self.num_of_items = int(re.findall("[0-9]+", parts[0])[0])
        self.dataset = parts[0]
        self.instance_info = parts[1]
        self.strategy = parts[3]
        
        if len(parts) > 4:
            self.relative_mistake = float(parts[3].replace(",", "."))
        else:
            self.relative_mistake = float(-1)

        self.full_path = full_path

class Solution:
    id: int
    count: int
    strategy: str
    max_value: int
    relative_mistake: float = None
    # Tuple of 1's and 0's
    things: Tuple[int] = None

    # Elapsed time in millis
    elapsed_time: float = None
    # Elapsed time in number of configurations
    elapsed_configs: int = None

    def __init__(self, task: Task, max_value: int, things, elapsed_configs: int = None, elapsed_time: float = None, relative_mistake: float = None):
        self.things = things
        self.max_value = max_value
        self.elapsed_configs = elapsed_configs
        self.elapsed_time = elapsed_time
        self.relative_mistake = relative_mistake
        self.id = task.id
        self.count = task.count
        self.strategy = task.strategy

    def output_str(self) -> str:
        output = f'{abs(self.id)} {self.count} {self.max_value} {self.strategy}'

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