from dataclasses import dataclass

@dataclass
class Thing:
    cost: int
    weight: int

@dataclass
class Task:
    id: int
    count: int
    capacity: int
    minValue: int
    things: [int]

@dataclass
class Solution:
    id: int
    count: int
    maxValue: int
    things: [int]