from myDataClasses import Task, Solution
from dataclasses import dataclass
from enum import Enum

@dataclass
class RecursiveResult:
    maxValue: int
    things: [int]

class Context():

    def __init__(self, strategy):
        self.strategy = strategy

    def solve(self, task: Task) -> Solution:
        return self.strategy.solve(task)

class SolverStrategy(object):
    
    def solve(self, task: Task) -> Solution:
        pass


class BruteForce(SolverStrategy):

    def recursiveSolve(self, task: Task, thingAtIndex: int, recursiveResult: RecursiveResult) -> RecursiveResult:
        if thingAtIndex >= task.count:
            # Last thing
            return NotImplemented

        return recursiveResult
    
    def solve(self, task: Task) -> Solution:
        print(f"BruteForce#{task.id} solving.")

        result = self.recursiveSolve(task, 0, RecursiveResult(0, []))

        return Solution(task.id, task.count, result.maxValue, result.things)

class BranchBorder(SolverStrategy):
    
    def solve(self, task: Task) -> Solution:
        print(f"BranchBorder#{task.id} solving.")

        return Solution(-1, -1, -1, [])

class Strategies(Enum):
    BruteForce = BruteForce()
    BranchBorder = BranchBorder()