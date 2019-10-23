from myDataClasses import Task, Solution, Thing, CostRow
from dataclasses import dataclass
from enum import Enum
from copy import deepcopy
from typing import List

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
    Uses DynamicProgramming recursive algorithm. 

    The DP table is a dictionary of rows. Keys are all possible sums of cost of different items. 
    
    Each row is a list with exactly (number_of_items + 1) members.

    Recursion:
    - W(0,0) = 0
    - W(0,c) = ∞ for all c > 0
    - W(i, c) = min(W(i-1, c), W(i-1, c-ci) + wi) for all i > 1.

    - c = current sum of costs
    - ci = cost of item at index i
    - wi = weight of item at index i
    - ∞ = infinity. Here it's (max(capacity, sum_of_all_weights) + 1)
    """

    def simplify_task(self, task: Task) -> bool:
        # Remove items with cost == 0 or weight > capacity
        self.work_things = [thing for thing in self.work_things if thing.cost > 0 and thing.weight <= task.capacity]
        self.work_count = len(self.work_things)

        return self.work_count != 0

    def prepare_table(self, task: Task) -> bool:
        """ Prepare the DP table & other important values """

        if not self.simplify_task(task):
            # No item can be added to the bag
            return False

        # The infinite value == (sum of all weights + 1)
        self.infinite_value = max(task.capacity, sum(thing.weight for thing in self.work_things)) + 1
        self.dp_table_dict = dict()
        
        # Add 0th row
        self.dp_table_dict[0] = CostRow(things_positions=tuple(), row=[0 for _ in range(self.work_count + 1)])
        
        count: int = 1
        max_count: int = pow(2, self.work_count)
        while count < max_count:
            # Get binary representation of count in a list
            bits = [int(bit) for bit in bin(count)[2:]]
            bits = list(reversed(bits))

            # Get sum of subset
            curr_sum: int = 0
            things_positions = list()
            for (i, bit) in enumerate(bits):
                if bit == 1:
                    curr_thing: Thing = self.work_things[i]
                    curr_sum += curr_thing.cost
                    things_positions.append(curr_thing.position)
            
            # Add row to the table
            if curr_sum not in self.dp_table_dict:
                row = [self.infinite_value]
                row.extend([None for _ in range(self.work_count)])
                self.dp_table_dict[curr_sum] = CostRow(things_positions=tuple(things_positions), row=row)

            count += 1

        return True

    def recursive_solve(self, dp_index: int, curr_sum: int,) -> int:
        """ Recursively find weight for the current position in the table. Returns the found weight. """

        cost_row: CostRow = self.dp_table_dict.get(curr_sum)

        if cost_row is None:
            # We requested a sum that is not possible to get with currently specified items. Return infinite
            return self.infinite_value

        if cost_row.row[dp_index] is not None:
            # Value is already in the table.
            return cost_row.row[dp_index]

        curr_thing: Thing = self.work_things[dp_index - 1]

        result: int = min(
            self.recursive_solve(dp_index - 1, curr_sum), 
            self.recursive_solve(dp_index - 1, curr_sum - curr_thing.cost) + curr_thing.weight
            )

        cost_row.row[dp_index] = result

        return result

    def construct_solution(self, task: Task, curr_sum: int) -> Solution:
        things_positions = self.dp_table_dict[curr_sum].things_positions
        things = [0 for _ in range(task.count)]
        max_sum = 0
        for pos in things_positions:
            things[pos] = 1
            max_sum += task.things[pos].cost
        return Solution(id=task.id, count=task.count, max_value=max_sum, relative_mistake=task.relative_mistake, things=things)

    def solve(self, task: Task) -> Solution:        
        self.work_count = task.count
        self.work_things = [Thing(thing.position, thing.weight, thing.cost) for thing in task.things]
        
        if not self.prepare_table(task):
            # No item can be added to the bag
            return self.construct_solution(task, 0)
        
        self.key_list = sorted(self.dp_table_dict, reverse=True)

        for curr_sum in self.key_list:
            # Recursively find the best value
            found_weight: int = self.recursive_solve(self.work_count, curr_sum)
            
            if found_weight <= task.capacity:
                # Found the highest value possible
                return self.construct_solution(task, curr_sum)

        return None

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

class GreedyOne(SolverStrategy):
    """ 
    Uses modified Greedy heuristics. 

    Things list are sorted by key cost in descending order. The list is iterated through and only 1 thing with the best
    cost possible is added to the bag. 
    
    """

    def solve(self, task: Task) -> Solution:
        # Sort things by cost comparison descending
        task.things = sorted(task.things, key=lambda thing: thing.cost, reverse=True)

        output_things = [0 for _ in task.things]
        max_value = 0

        for thing in task.things:
            if thing.weight <= task.capacity:
                output_things[thing.position] = 1
                max_value = thing.cost
                break
            print
        
        return Solution(id=task.id, count=task.count, max_value=max_value, relative_mistake=task.relative_mistake, things=tuple(output_things))

class FPTAS(SolverStrategy):
    """ 
    Uses FPTAS algorithm. 

    Uses provided value e (relative mistake) to make the task simpler. 
    Specifically, it is used to lower costs of all items.
    The simplified task is then passed to DP algorithm.
    
    """

    def get_column_descriptions(self, show_time: bool = True):
        output = super().get_column_descriptions(show_time)

        output.insert(output.index("|"), "relative_error")

        return output

    def solve(self, task: Task) -> Solution:
        # Prepare important constants
        max_cost = max([thing.cost for thing in task.things])
        simplifier_constant: float = (task.relative_mistake*max_cost)/task.count

        # Create simplified task
        simplified_task: Task = Task(id=task.id, count=task.count, capacity=task.capacity, relative_mistake=task.relative_mistake, things=deepcopy(task.things))
        for thing in simplified_task.things:
            thing.cost = int(thing.cost // simplifier_constant)

        # Use DP on the simplified solution
        solution: Solution = Strategies.DP.value.solve(simplified_task)

        # Get non-updated maximum value
        max_value = 0
        for (i, bit) in enumerate(solution.things):
            if bit == 1:
                max_value += task.things[i].cost
        solution.max_value = max_value

        return solution

class Strategies(Enum):
    DP = DynamicProgramming()
    DP_Weight = DynamicProgramming_Weight()
    Greedy = Greedy()
    GreedyOne = GreedyOne()
    FPTAS = FPTAS()

# class BranchBound(SolverStrategy):
#     """ Uses BranchBound algorithm. """

#     def getMaxSum(self, task: Task) -> int:
#         currSum = 0
#         for thing in reversed(task.things):
#             currSum += thing.cost

#         return currSum
    
#     # maximumSum: A sum of all objects that are after the current object
#     def recursiveSolve(self, mode, configCtr: ConfigCounter, task: Task, maximumSum: int, thingAtIndex: int, currState: RecursiveResult) -> RecursiveResult:
#         if mode == Modes.Decision and currState.max_value >= task.minValue:
#             # Found good enough value
#             return currState
        
#         configCtr.value += 1
#         currThing = task.things[thingAtIndex]
#         if thingAtIndex >= task.count - 1:
#             # Last thing
#             if currThing.weight <= currState.remainingCapacity:
#                 return currState.newSolution(currThing)
#             else:
#                 return currState.newSolution()
        
#         # Check all possibilities
#         if currThing.weight <= currState.remainingCapacity:
#             if mode == Modes.Decision and maximumSum + currState.max_value < task.minValue:
#                 # Value of (things in bag + current thing + all things in the subtree) is not high enough
#                 return currState
            
#             # The subtree has high enough value, need to check if things can fit
#             resultAdded = self.recursiveSolve(configCtr, mode, task, maximumSum - currThing.cost, thingAtIndex + 1, currState.newSolution(currThing))
            
#             if resultAdded.max_value >= currState.max_value + maximumSum - currThing.cost:
#                 # The max_value of the entire branch where this item was not added is not high enough
#                 # so we do not need to check it
#                 return resultAdded

#             if mode == Modes.Decision:
#                 if resultAdded.max_value >= task.minValue:
#                     # Found good enough value
#                     return resultAdded
#                 elif maximumSum - currThing.cost + currState.max_value < task.minValue:
#                     # Value of (things in bag + all things in the subtree) is not high enough
#                     return currState
            
#             # The subtree has high enough value, need to check if things can fit
#             resultNotAdded = self.recursiveSolve(configCtr, mode, task, maximumSum - currThing.cost, thingAtIndex + 1, currState.newSolution())
            
#             if resultAdded.max_value >= resultNotAdded.max_value:
#                 return resultAdded.newSolution()
#             else:
#                 return resultNotAdded.newSolution()

#         if mode == Modes.Decision and maximumSum - currThing.cost + currState.max_value < task.minValue:
#                 # Value of (things in bag + all things in the subtree) is not high enough
#                 return currState        
        
#         # Current thing too heavy. The subtree has high enough value, need to check if items fit
#         return self.recursiveSolve(configCtr, mode, task, maximumSum - currThing.cost, thingAtIndex + 1, currState.newSolution())
    
#     def solve(self, task: Task) -> Solution:
#         # print(f"BranchBound#{task.id} solving.")

#         # Sort things by cost/weight comparison
#         task.things = sorted(task.things, key=lambda thing: thing.cost/thing.weight, reverse=True)

#         # Create a descending list of maximum sums that is going to be used for value-based decisions in BranchBound alg.
#         maximumSum = self.getMaxSum(task)
#         configCtr = ConfigCounter(0)
#         mode = None
#         result = self.recursiveSolve(mode, configCtr, task, maximumSum, 0, RecursiveResult(task.capacity, 0, [0 for i in task.things]))

#         return Solution(task.id, task.count, result.max_value, task.minValue, configCtr.value, result.things)