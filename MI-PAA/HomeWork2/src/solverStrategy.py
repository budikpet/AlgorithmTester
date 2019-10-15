from myDataClasses import Task, Solution, Thing, Modes
from dataclasses import dataclass
from enum import Enum
from copy import deepcopy
from typing import List

@dataclass
class ConfigCounter:
    value: int

@dataclass
class RecursiveResult:
    remainingCapacity: int
    maxValue: int
    things: List[int]

    def newSolution(self, thing: Thing = None):        
        if thing is not None:
            things = deepcopy(self.things)
            things[thing.position] = 1
            return RecursiveResult(self.remainingCapacity - thing.weight, self.maxValue + thing.cost, things)
        else:
            return RecursiveResult(self.remainingCapacity, self.maxValue, deepcopy(self.things))

class Context():

    def __init__(self, strategy):
        self.strategy = strategy

    def solve(self, task: Task) -> Solution:
        return self.strategy.solve(task)

class SolverStrategy(object):
    
    def solve(self, task: Task) -> Solution:
        pass

class DynamicProgramming(SolverStrategy):
    """ Uses DynamicProgramming algorithm. """

    def solve(self, task: Task) -> Solution:
        pass

class GreedySimple(SolverStrategy):
    """ Uses simple Greedy heuristics. """

    def solve(self, task: Task) -> Solution:
        pass

class Greedy(SolverStrategy):
    """ Uses modified Greedy heuristics. """

    def solve(self, task: Task) -> Solution:
        pass

class FPTAS(SolverStrategy):
    """ Uses FPTAS algorithm. """

    def solve(self, task: Task) -> Solution:
        pass

class Strategies(Enum):
    DP = DynamicProgramming()
    GreedySimple = GreedySimple()
    Greedy = Greedy()
    FPTAS = FPTAS()

class BranchBound(SolverStrategy):
    """ Uses BranchBound algorithm. """

    def getMaxSum(self, task: Task) -> int:
        currSum = 0
        for thing in reversed(task.things):
            currSum += thing.cost

        return currSum
    
    # maximumSum: A sum of all objects that are after the current object
    def recursiveSolve(self, mode, configCtr: ConfigCounter, task: Task, maximumSum: int, thingAtIndex: int, currState: RecursiveResult) -> RecursiveResult:
        if mode == Modes.Decision and currState.maxValue >= task.minValue:
            # Found good enough value
            return currState
        
        configCtr.value += 1
        currThing = task.things[thingAtIndex]
        if thingAtIndex >= task.count - 1:
            # Last thing
            if currThing.weight <= currState.remainingCapacity:
                return currState.newSolution(currThing)
            else:
                return currState.newSolution()
        
        # Check all possibilities
        if currThing.weight <= currState.remainingCapacity:
            if mode == Modes.Decision and maximumSum + currState.maxValue < task.minValue:
                # Value of (things in bag + current thing + all things in the subtree) is not high enough
                return currState
            
            # The subtree has high enough value, need to check if things can fit
            resultAdded = self.recursiveSolve(configCtr, mode, task, maximumSum - currThing.cost, thingAtIndex + 1, currState.newSolution(currThing))
            
            if resultAdded.maxValue >= currState.maxValue + maximumSum - currThing.cost:
                # The maxValue of the entire branch where this item was not added is not high enough
                # so we do not need to check it
                return resultAdded

            if mode == Modes.Decision:
                if resultAdded.maxValue >= task.minValue:
                    # Found good enough value
                    return resultAdded
                elif maximumSum - currThing.cost + currState.maxValue < task.minValue:
                    # Value of (things in bag + all things in the subtree) is not high enough
                    return currState
            
            # The subtree has high enough value, need to check if things can fit
            resultNotAdded = self.recursiveSolve(configCtr, mode, task, maximumSum - currThing.cost, thingAtIndex + 1, currState.newSolution())
            
            if resultAdded.maxValue >= resultNotAdded.maxValue:
                return resultAdded.newSolution()
            else:
                return resultNotAdded.newSolution()

        if mode == Modes.Decision and maximumSum - currThing.cost + currState.maxValue < task.minValue:
                # Value of (things in bag + all things in the subtree) is not high enough
                return currState        
        
        # Current thing too heavy. The subtree has high enough value, need to check if items fit
        return self.recursiveSolve(configCtr, mode, task, maximumSum - currThing.cost, thingAtIndex + 1, currState.newSolution())
    
    def solve(self, task: Task) -> Solution:
        # print(f"BranchBound#{task.id} solving.")

        # Sort things by cost/weight comparison
        task.things = sorted(task.things, key=lambda thing: thing.cost/thing.weight, reverse=True)

        # Create a descending list of maximum sums that is going to be used for value-based decisions in BranchBound alg.
        maximumSum = self.getMaxSum(task)
        configCtr = ConfigCounter(0)
        mode = None
        result = self.recursiveSolve(mode, configCtr, task, maximumSum, 0, RecursiveResult(task.capacity, 0, [0 for i in task.things]))

        return Solution(task.id, task.count, result.maxValue, task.minValue, configCtr.value, result.things)