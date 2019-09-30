from myDataClasses import Task, Solution
from enum import Enum

class Context():

    def __init__(self, strategy):
        self.strategy = strategy

    def solve(self, task: Task) -> Solution:
        return self.strategy.solve(task)

class SolverStrategy(object):
    
    def solve(self, task: Task) -> Solution:
        pass


class BruteForce(SolverStrategy):
    
    def solve(self, task: Task) -> Solution:
        print(f"BruteForce#{task.id} solving.")

        return Solution(-1, -1, -1, [])

class BranchBorder(SolverStrategy):
    
    def solve(self, task: Task) -> Solution:
        print(f"BranchBorder#{task.id} solving.")

        return Solution(-1, -1, -1, [])

class Strategies(Enum):
    BruteForce = BruteForce()
    BranchBorder = BranchBorder()