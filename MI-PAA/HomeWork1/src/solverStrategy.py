from myDataClasses import Task, Solution, Thing, Modes
from dataclasses import dataclass
from enum import Enum
from copy import deepcopy
from typing import List

@dataclass
class RecursiveResult:
    remainingCapacity: int
    maxValue: int
    things: List[int]
    numberOfConfigurations: int     # Number of final solutions that were visited

    def newSolution(self, thing: Thing = None, configurationsToAdd: int = 0):        
        if thing is not None:
            things = deepcopy(self.things)
            things[thing.position] = 1
            return RecursiveResult(self.remainingCapacity - thing.weight, self.maxValue + thing.cost, things, self.numberOfConfigurations + configurationsToAdd)
        else:
            return RecursiveResult(self.remainingCapacity, self.maxValue, deepcopy(self.things), self.numberOfConfigurations + configurationsToAdd)

class Context():

    def __init__(self, mode, strategy):
        self.mode = mode
        self.strategy = strategy

    def solve(self, task: Task) -> Solution:
        return self.strategy.solve(self.mode, task)

class SolverStrategy(object):
    
    def solve(self, Modes: str, task: Task) -> Solution:
        pass


class BruteForce(SolverStrategy):
    """ Uses Brute force  """

    def recursiveSolve(self, mode: Modes, task: Task, thingAtIndex: int, currState: RecursiveResult) -> RecursiveResult:
        if mode == Modes.Decision:
            if currState.maxValue >= task.minValue:
                return currState
        
        currThing = task.things[thingAtIndex]
        if thingAtIndex >= task.count - 1:
            # Last thing
            if currThing.weight <= currState.remainingCapacity:
                return currState.newSolution(currThing, configurationsToAdd=1)
            else:
                return currState.newSolution(configurationsToAdd=1)
        
        # Check all possibilities
        if currThing.weight <= currState.remainingCapacity:
            # Can add current thing
            resultAdded = self.recursiveSolve(mode, task, thingAtIndex + 1, currState.newSolution(currThing))
            
            if mode == Modes.Decision and resultAdded.maxValue >= task.minValue:
                # Found good enough value
                return resultAdded
            
            resultNotAdded = self.recursiveSolve(mode, task, thingAtIndex + 1, currState.newSolution())
            
            if resultAdded.maxValue >= resultNotAdded.maxValue:
                return resultAdded.newSolution(configurationsToAdd=resultNotAdded.numberOfConfigurations)
            else:
                return resultNotAdded.newSolution(configurationsToAdd=resultAdded.numberOfConfigurations)
        
        return self.recursiveSolve(mode, task, thingAtIndex + 1, currState.newSolution())
    
    def solve(self, mode: Modes, task: Task) -> Solution:
        # print(f"BruteForce#{task.id} solving.")

        result = self.recursiveSolve(mode, task, 0, RecursiveResult(task.capacity, 0, [0 for i in task.things], 0))

        return Solution(task.id, task.count, result.maxValue, task.minValue, result.numberOfConfigurations, result.things)

class BranchBound(SolverStrategy):
    """ Uses BranchBound algorithm. """

    def getMaxSum(self, task: Task) -> int:
        currSum = 0
        for thing in reversed(task.things):
            currSum += thing.cost

        return currSum
    
    # maximumSum: A sum of all objects that are after the current object
    def recursiveSolve(self, mode: Modes, task: Task, maximumSum: int, thingAtIndex: int, currState: RecursiveResult) -> RecursiveResult:
        if mode == Modes.Decision and currState.maxValue >= task.minValue:
            # Found good enough value
            return currState
        
        currThing = task.things[thingAtIndex]
        if thingAtIndex >= task.count - 1:
            # Last thing
            if currThing.weight <= currState.remainingCapacity:
                return currState.newSolution(currThing, configurationsToAdd=1)
            else:
                return currState.newSolution(configurationsToAdd=1)
        
        # Check all possibilities
        if currThing.weight <= currState.remainingCapacity:
            # Can add current thing
            resultAdded = self.recursiveSolve(mode, task, maximumSum - currThing.cost, thingAtIndex + 1, currState.newSolution(currThing))
            
            if resultAdded.maxValue >= currState.maxValue + maximumSum - currThing.cost:
                # The maxValue of the entire branch where this item was not added is not high enough
                # so we do not need to check it
                return resultAdded

            if mode == Modes.Decision and resultAdded.maxValue >= task.minValue:
                # Found good enough value
                return resultAdded
            
            resultNotAdded = self.recursiveSolve(mode, task, maximumSum - currThing.cost, thingAtIndex + 1, currState.newSolution())
            
            if resultAdded.maxValue >= resultNotAdded.maxValue:
                return resultAdded.newSolution(configurationsToAdd=resultNotAdded.numberOfConfigurations)
            else:
                return resultNotAdded.newSolution(configurationsToAdd=resultAdded.numberOfConfigurations)
        
        # Current thing too heavy
        return self.recursiveSolve(mode, task, maximumSum - currThing.cost, thingAtIndex + 1, currState.newSolution())
    
    def solve(self, mode: Modes, task: Task) -> Solution:
        # print(f"BranchBound#{task.id} solving.")

        # Sort things by cost/weight comparison
        task.things = sorted(task.things, key=lambda thing: thing.cost/thing.weight, reverse=True)

        # Create a descending list of maximum sums that is going to be used for value-based decisions in BranchBound alg.
        maximumSum = self.getMaxSum(task)
        result = self.recursiveSolve(mode, task, maximumSum, 0, RecursiveResult(task.capacity, 0, [0 for i in task.things], 0))

        return Solution(task.id, task.count, result.maxValue, task.minValue, result.numberOfConfigurations, result.things)

class UnsortedBranchBound(SolverStrategy):
    """ Uses BranchBound algorithm without sorting the input first. """
    
    def solve(self, mode: Modes, task: Task) -> Solution:
        # print(f"UnsortedBranchBound#{task.id} solving.")
        solver = Strategies.BranchBound.value

        # Create a descending list of maximum sums that is going to be used for value-based decisions in BranchBound alg.
        maximumSum = solver.getMaxSum(task)
        result = solver.recursiveSolve(mode, task, maximumSum, 0, RecursiveResult(task.capacity, 0, [0 for i in task.things], 0))

        return Solution(task.id, task.count, result.maxValue, task.minValue, result.numberOfConfigurations, result.things)

class Strategies(Enum):
    BruteForce = BruteForce()
    BranchBound = BranchBound()
    UnsortedBranchBound = UnsortedBranchBound()