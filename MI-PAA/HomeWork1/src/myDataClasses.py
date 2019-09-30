from dataclasses import dataclass

@dataclass
class Task:
    id: int
    count: int
    capacity: int
    minValue: int
    thingValues: [int]

@dataclass
class Solution:
    id: int
    count: int
    bestValue: int
    things: [int]