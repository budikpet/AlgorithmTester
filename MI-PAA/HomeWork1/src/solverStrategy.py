from myDataClasses import Task, Solution, Thing
from dataclasses import dataclass
from enum import Enum

@dataclass
class RecursiveResult:
    remainingCapacity: int
    maxValue: int
    things: [int]
    numberOfConfigurations: int     # Number of final solutions that were visited

    def newSolution(self, thing: Thing = None, configurationsToAdd: int = 0):        
        if thing is not None:
            things = self.things
            things[thing.position] = 1
            return RecursiveResult(self.remainingCapacity - thing.weight, self.maxValue + thing.cost, things, self.numberOfConfigurations + configurationsToAdd)
        else:
            return RecursiveResult(self.remainingCapacity, self.maxValue, self.things, self.numberOfConfigurations + configurationsToAdd)

class Context():

    def __init__(self, strategy):
        self.strategy = strategy

    def solve(self, task: Task) -> Solution:
        return self.strategy.solve(task)

class SolverStrategy(object):
    
    def solve(self, task: Task) -> Solution:
        pass


class BruteForce(SolverStrategy):
    """ Uses Brute force  """

    def recursiveSolve(self, task: Task, thingAtIndex: int, currState: RecursiveResult) -> RecursiveResult:
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
            resultAdded = self.recursiveSolve(task, thingAtIndex + 1, currState.newSolution(currThing))
            resultNotAdded = self.recursiveSolve(task, thingAtIndex + 1, currState.newSolution())
            
            if resultAdded.maxValue >= resultNotAdded.maxValue:
                return resultAdded.newSolution(configurationsToAdd=resultNotAdded.numberOfConfigurations)
            else:
                return resultNotAdded.newSolution(configurationsToAdd=resultAdded.numberOfConfigurations)
        
        return self.recursiveSolve(task, thingAtIndex + 1, currState.newSolution())
    
    def solve(self, task: Task) -> Solution:
        # print(f"BruteForce#{task.id} solving.")

        result = self.recursiveSolve(task, 0, RecursiveResult(task.capacity, 0, [0 for i in task.things], 0))

        return Solution(task.id, task.count, result.maxValue, result.numberOfConfigurations, result.things)

class BranchBound(SolverStrategy):
    """ Uses BranchBound algorithm. """

    def getMaxSumsTuple(self, task: Task):
        maximumSums = list()
        currSum = 0
        for thing in reversed(task.things):
            currSum += thing.cost
            maximumSums.append(currSum)

        return tuple(reversed(maximumSums))
    
    def recursiveSolve(self, task: Task, maximumSums: (int), thingAtIndex: int, currState: RecursiveResult) -> RecursiveResult:
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
            resultAdded = self.recursiveSolve(task, maximumSums, thingAtIndex + 1, currState.newSolution(currThing))
            
            if resultAdded.maxValue >= currState.maxValue + maximumSums[thingAtIndex + 1]:
                # The maxValue of the entire branch where this item was not added is not high enough
                # so we do not need to check it
                return resultAdded
            
            resultNotAdded = self.recursiveSolve(task, maximumSums, thingAtIndex + 1, currState.newSolution())
            
            if resultAdded.maxValue >= resultNotAdded.maxValue:
                return resultAdded.newSolution(configurationsToAdd=resultNotAdded.numberOfConfigurations)
            else:
                return resultNotAdded.newSolution(configurationsToAdd=resultAdded.numberOfConfigurations)
        
        # Current thing too heavy
        return self.recursiveSolve(task, maximumSums, thingAtIndex + 1, currState.newSolution())
    
    def solve(self, task: Task) -> Solution:
        # print(f"BranchBound#{task.id} solving.")

        # Sort things by cost/weight comparison
        task.things = sorted(task.things, key=lambda thing: thing.cost/thing.weight, reverse=True)

        # Create a descending list of maximum sums that is going to be used for value-based decisions in BranchBound alg.
        maximumSums = self.getMaxSumsTuple(task)
        result = self.recursiveSolve(task, maximumSums, 0, RecursiveResult(task.capacity, 0, [0 for i in task.things], 0))

        return Solution(task.id, task.count, result.maxValue, result.numberOfConfigurations, result.things)

class UnsortedBranchBound(SolverStrategy):
    """ Uses BranchBound algorithm without sorting the input first. """
    def solve(self, task: Task) -> Solution:
        # print(f"UnsortedBranchBound#{task.id} solving.")
        solver = Strategies.BranchBound.value

        # Create a descending list of maximum sums that is going to be used for value-based decisions in BranchBound alg.
        maximumSums = solver.getMaxSumsTuple(task)
        result = solver.recursiveSolve(task, maximumSums, 0, RecursiveResult(task.capacity, 0, [0 for i in task.things], 0))

        return Solution(task.id, task.count, result.maxValue, result.numberOfConfigurations, result.things)

class Strategies(Enum):
    BruteForce = BruteForce()
    BranchBound = BranchBound()
    UnsortedBranchBound = UnsortedBranchBound()