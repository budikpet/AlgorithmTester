from dataclasses import dataclass
from enum import Enum
from copy import deepcopy
from typing import List
import numpy as np
from algorithm_tester.myDataClasses import Task, Solution, Thing

class Context():

    def __init__(self, strategy):
        self.strategy = strategy

    def solve(self, task: Task) -> Solution:
        return self.strategy.solve(task)

class SolverStrategy(object):

    def get_column_descriptions(self, show_time: bool = True):
        output = [
            "id",
            "item_count",
            "maximum_sum",
            "|",
            "items_in_bag"
        ]

        if show_time:
            output.insert(output.index("|"), "time")

        return output
    
    def solve(self, task: Task) -> Solution:
        pass

class BruteForce(SolverStrategy):
    """ Uses Brute force  """

    def recursiveSolve(self, configCtr: ConfigCounter, mode: Modes, task: Task, thingAtIndex: int, currState: RecursiveResult) -> RecursiveResult:
        if mode == Modes.Decision:
            if currState.maxValue >= task.minValue:
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
            # Can add current thing
            resultAdded = self.recursiveSolve(configCtr, mode, task, thingAtIndex + 1, currState.newSolution(currThing))
            
            if mode == Modes.Decision and resultAdded.maxValue >= task.minValue:
                # Found good enough value
                return resultAdded.newSolution()
            
            resultNotAdded = self.recursiveSolve(configCtr, mode, task, thingAtIndex + 1, currState.newSolution())
            
            if resultAdded.maxValue >= resultNotAdded.maxValue:
                return resultAdded.newSolution()
            else:
                return resultNotAdded.newSolution()
        
        return self.recursiveSolve(configCtr, mode, task, thingAtIndex + 1, currState.newSolution())
    
    def solve(self, mode: Modes, task: Task) -> Solution:
        # print(f"BruteForce#{task.id} solving.")

        # Sort things by cost/weight comparison
        task.things = sorted(task.things, key=lambda thing: thing.cost/thing.weight, reverse=True)

        configCtr = ConfigCounter(0)
        result = self.recursiveSolve(configCtr, mode, task, 0, RecursiveResult(task.capacity, 0, [0 for i in task.things]))

        return Solution(task.id, task.count, result.maxValue, task.minValue, configCtr.value, result.things)

class BranchBound(SolverStrategy):
    """ Uses BranchBound algorithm. """

    def getMaxSum(self, task: Task) -> int:
        currSum = 0
        for thing in reversed(task.things):
            currSum += thing.cost

        return currSum
    
    # maximumSum: A sum of all objects that are after the current object
    def recursiveSolve(self, configCtr: ConfigCounter, mode: Modes, task: Task, maximumSum: int, thingAtIndex: int, currState: RecursiveResult) -> RecursiveResult:
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
                # so we do not need to check it
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
    
    def solve(self, mode: Modes, task: Task) -> Solution:
        # print(f"BranchBound#{task.id} solving.")

        # Sort things by cost/weight comparison
        task.things = sorted(task.things, key=lambda thing: thing.cost/thing.weight, reverse=True)

        # Create a descending list of maximum sums that is going to be used for value-based decisions in BranchBound alg.
        maximumSum = self.getMaxSum(task)
        configCtr = ConfigCounter(0)
        result = self.recursiveSolve(configCtr, mode, task, maximumSum, 0, RecursiveResult(task.capacity, 0, [0 for i in task.things]))

        return Solution(task.id, task.count, result.maxValue, task.minValue, configCtr.value, result.things)

class UnsortedBranchBound(SolverStrategy):
    """ Uses BranchBound algorithm without sorting the input first. """
    
    def solve(self, mode: Modes, task: Task) -> Solution:
        # print(f"UnsortedBranchBound#{task.id} solving.")
        solver = Strategies.BranchBound.value

        # Create a descending list of maximum sums that is going to be used for value-based decisions in BranchBound alg.
        maximumSum = solver.getMaxSum(task)
        configCtr = ConfigCounter(0)
        result = solver.recursiveSolve(configCtr, mode, task, maximumSum, 0, RecursiveResult(task.capacity, 0, [0 for i in task.things]))

        return Solution(task.id, task.count, result.maxValue, task.minValue, configCtr.value, result.things)

class DynamicProgramming_Weight(SolverStrategy):
    """ 
    Uses DynamicProgramming iterative algorithm. 

    The DP table is a 2D table. Number of rows == capacity. 
    Each row is a list with exactly (number_of_items + 1) members.

    Algorithm fills the table from the bottom up.

    """

    def get_solution(self, task: Task):
        # Get the best possible value
        for i in range(1, task.count+1): 
            for w in range(1, task.capacity+1): 
                last_thing: Thing = task.things[i-1]
                if last_thing.weight <= w: 
                    # Possible to add thing to the bag
                    self.dp_table[i][w] = max(last_thing.cost + self.dp_table[i-1][w-last_thing.weight], self.dp_table[i-1][w]) 
                else: 
                    self.dp_table[i][w] = self.dp_table[i-1][w]
        
        best_value = self.dp_table[task.count][task.capacity]
        
        # Get things in the bag
        remaining_value: int = best_value
        output_things = [0 for i in range(task.count)]
        
        for i in reversed(range(task.count)):
            row = self.dp_table[i]
            
            if remaining_value not in row:
                # The remaining_value is not present in i-th row so it came with i-th item
                thing: Thing = task.things[i]
                remaining_value -= thing.cost
                output_things[thing.position] = 1

            if remaining_value == 0:
                break

        return Solution(id=task.id, count=task.count, max_value=best_value, things=tuple(output_things))

    def prepare_table(self, task: Task):
        dummy_row = [None for i in range(task.capacity + 1)]
        dummy_row[0] = 0

        self.dp_table = [[0 for i in range(task.capacity + 1)]]
        self.dp_table.extend([deepcopy(dummy_row) for i in range(task.count)])

    def solve(self, task: Task) -> Solution:
        self.prepare_table(task)
        return self.get_solution(task)

class DynamicProgramming(SolverStrategy):
    """ 
    Uses DynamicProgramming iterative algorithm. 

    Uses a DP table – a 2D MxN table. W(i, c) is a weight of filled knapsack when only the first i number of items are considered.
    The table is filled according to Rules.

    The table is built from bottom up.
    
    Rules:
    - W(0,0) = 0
    - W(0,c) = ∞ for all c > 0
    - W(i, c) = min(W(i-1, c), W(i-1, c-ci) + wi) for all i > 1.

    - c = current sum of costs
    - ci = cost of item at index i
    - wi = weight of item at index i
    - ∞ = infinity. Here it's (max(capacity, sum_of_all_weights) + 1)
    - M = sum of costs of all things available
    """

    def simplify_task(self, task: Task) -> bool:
        # Remove items with cost == 0 or weight > capacity
        self.work_things = [thing for thing in self.work_things if thing.cost > 0 and thing.weight <= task.capacity]
        self.work_count = len(self.work_things)

        return self.work_count != 0

    def get_max_values(self):
        max_cost_sum, max_weight_sum = 0, 0
        for thing in self.work_things:
            max_cost_sum += thing.cost
            max_weight_sum += thing.weight
        return max_cost_sum, max_weight_sum

    def prepare_table(self, task: Task) -> bool:
        """ Prepare the DP table & other important values """

        # if not self.simplify_task(task):
        #     # No item can be added to the bag
        #     return False

        # The infinite value == (sum of all weights + 1)
        self.max_cost_sum, max_weight_sum = self.get_max_values() 
        self.infinite_value = max(task.capacity, max_weight_sum) + 1
        
        # Create dp_table
        self.dp_table = np.zeros((self.max_cost_sum + 1, self.work_count + 1))
        self.dp_table[:,0] = self.infinite_value
        self.dp_table[0,0] = 0

        return True

    def construct_solution(self, task: Task, found_sum: int, found_weight: int) -> Solution:
        """ Reconstructs vector of things using the filled table. """
        things_positions = list()
        curr_sum = found_sum
        curr_weight = found_weight
        for row_index in reversed(range(1, self.work_count + 1)):
            if self.dp_table[curr_sum][row_index] != self.dp_table[curr_sum][row_index - 1]:
                # Thing at row_index is in the bag
                curr_thing: Thing = self.work_things[row_index - 1]
                things_positions.append(curr_thing.position)
                curr_weight -= curr_thing.weight
                curr_sum -= curr_thing.cost

            if curr_weight == 0:
                break

        things = [0 for _ in range(task.count)]
        for pos in things_positions:
            things[pos] = 1

        return Solution(id=task.id, count=task.count, max_value=found_sum, relative_mistake=task.relative_mistake, things=tuple(things))

    def solve(self, task: Task) -> Solution:        
        self.work_count = task.count
        self.work_things = [Thing(thing.position, thing.weight, thing.cost) for thing in task.things]
        
        if not self.prepare_table(task):
            # No item can be added to the bag
            return Solution(id=task.id, count=task.count, max_value=0, relative_mistake=task.relative_mistake, things=tuple(0 for _ in range(task.count)))
        
        best_sum = 0
        for curr_sum in range(1, self.max_cost_sum + 1):
            for i in range(1, self.work_count + 1):
                result1, result2 = self.dp_table[curr_sum][i - 1], self.infinite_value
                curr_thing: Thing = self.work_things[i - 1]
                if curr_sum - curr_thing.cost >= 0:
                    result2 = self.dp_table[curr_sum - curr_thing.cost][i - 1] + curr_thing.weight

                self.dp_table[curr_sum][i] = min(result1, result2)
            
            if self.dp_table[curr_sum][i] <= task.capacity:
                best_sum = curr_sum

        return self.construct_solution(task, best_sum, self.dp_table[best_sum][self.work_count])

class Greedy(SolverStrategy):
    """ 
    Uses simple Greedy heuristics. 

    Things list are sorted by key (cost/weight) in descending order. The list is iterated through and things are added to the bag
    if they fit.
    
    """
    def solve(self, task: Task) -> Solution:
        # Sort things by cost/weight comparison descending
        task.things = sorted(task.things, key=lambda thing: thing.cost/thing.weight, reverse=True)

        output_things = [0 for _ in task.things]
        max_sum = 0
        remaining_capacity = task.capacity

        # Find solution
        for thing in task.things:
            if thing.weight <= remaining_capacity:
                remaining_capacity -= thing.weight
                max_sum += thing.cost
                output_things[thing.position] = 1

            if remaining_capacity <= 0:
                break
            print

        return Solution(id=task.id, count=task.count, max_value=max_sum, relative_mistake=task.relative_mistake, things=tuple(output_things))

class Strategies(Enum):
    Brute = BruteForce()
    BB = BranchBound()
    UBB = UnsortedBranchBound()
    DP = DynamicProgramming()
    DPWeight = DynamicProgramming_Weight()
    Greedy = Greedy()