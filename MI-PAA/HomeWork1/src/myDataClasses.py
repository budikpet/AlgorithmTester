from dataclasses import dataclass, field
from typing import List

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
    minValue: int
    things: List[Thing] = field(default_factory=list)

@dataclass
class Solution:
    id: int
    count: int
    maxValue: int
    requestedMinValue: int
    numberOfConfigurations: int
    things: [int] = field(default_factory=list)

    def __str__(self):
        return f'{abs(self.id)} {self.numberOfConfigurations} {self.count} {self.maxValue} {self.requestedMinValue} | {" ".join(map(str, self.things))}'

    def __repr__(self):
        return self.__str__()