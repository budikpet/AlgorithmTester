from dataclasses import dataclass, field
from typing import List
from enum import Enum

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
    things: List[Thing] = field(default_factory=list)

@dataclass
class CostRow:
    things: tuple = field(default_factory=tuple)
    row: list = field(default_factory=list)

@dataclass
class Solution:
    id: int
    count: int
    max_value: int
    # Elapsed time in millis
    elapsed_time: float = None
    # Tuple of 1's and 0's
    things: tuple = field(default_factory=tuple)

    def __str__(self):
        if self.elapsed_time is None:
            return f'{abs(self.id)} {self.count} {self.max_value} | {" ".join(map(str, self.things))}'
        else:
            return f'{abs(self.id)} {self.count} {self.max_value} {self.elapsed_time} | {" ".join(map(str, self.things))}'

    def __repr__(self):
        return self.__str__()