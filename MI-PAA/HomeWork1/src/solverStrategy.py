from myDataClasses import Task, Solution, Thing
from dataclasses import dataclass
from enum import Enum

@dataclass
class RecursiveResult:
    remainingCapacity: int
    maxValue: int
    things: [int]

    def newSolution(self, thing: Thing = None):
        if thing is not None:
            return RecursiveResult(self.remainingCapacity - thing.weight, self.maxValue + thing.cost, self.things + [1])
        else:
            return RecursiveResult(self.remainingCapacity, self.maxValue, self.things + [0])

class Context():

    def __init__(self, strategy):
        self.strategy = strategy

    def solve(self, task: Task) -> Solution:
        return self.strategy.solve(task)

class SolverStrategy(object):
    
    def solve(self, task: Task) -> Solution:
        pass


class BruteForce(SolverStrategy):

    def recursiveSolve(self, task: Task, thingAtIndex: int, currState: RecursiveResult) -> RecursiveResult:
        currThing = task.things[thingAtIndex]
        if thingAtIndex >= task.count - 1:
            # Last thing
            if currThing.weight <= currState.remainingCapacity:
                return currState.newSolution(currThing)
            else:
                return currState.newSolution()
        
        # Check all possibilities
        if currThing.weight <= currState.remainingCapacity:
            # Can add current thing
            resultAdded = self.recursiveSolve(task, thingAtIndex + 1, currState.newSolution(currThing))
            resultNotAdded = self.recursiveSolve(task, thingAtIndex + 1, currState.newSolution())
            return (resultAdded if resultAdded.maxValue >= resultNotAdded.maxValue else resultNotAdded)
        
        return self.recursiveSolve(task, thingAtIndex + 1, currState.newSolution())
    
    def solve(self, task: Task) -> Solution:
        # print(f"BruteForce#{task.id} solving.")

        result = self.recursiveSolve(task, 0, RecursiveResult(task.capacity, 0, list()))

        return Solution(task.id, task.count, result.maxValue, result.things)

class BranchBorder(SolverStrategy):
    
    def solve(self, task: Task) -> Solution:
        print(f"BranchBorder#{task.id} solving.")

        return Solution(-1, -1, -1, [])

class Strategies(Enum):
    BruteForce = BruteForce()
    BranchBorder = BranchBorder()