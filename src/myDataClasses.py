from dataclasses import dataclass, field
from typing import List
from enum import Enum
import re

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
    # None if not used
    relative_mistake: float
    things: List[Thing] = field(default_factory=list)

class AnalysisFile:

    def __init__(self, filename: str, full_path: str):
        parts = filename.replace(".dat", "").split("_")
        self.num_of_items = int(re.findall("[0-9]+", parts[0])[0])
        self.dataset = parts[0].replace(f"{self.num_of_items}", "")
        self.strategy = parts[2]
        
        if len(parts) > 3:
            self.relative_mistake = float(parts[3].replace(",", "."))
        else:
            self.relative_mistake = float(-1)

        self.full_path = full_path

@dataclass
class Solution:
    id: int
    count: int
    max_value: int
    relative_mistake: float = None
    # Elapsed time in millis
    elapsed_time: float = None
    # Tuple of 1's and 0's
    things: tuple = field(default_factory=tuple)

    def __str__(self):
        output = f'{abs(self.id)} {self.count} {self.max_value}'

        if self.elapsed_time is not None:
            output = f'{output} {self.elapsed_time}'

        if self.relative_mistake is not None:
            output = f'{output} {self.relative_mistake}'

        return f'{output} | {" ".join(map(str, self.things))}'

    def __repr__(self):
        return self.__str__()