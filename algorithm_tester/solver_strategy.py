from dataclasses import dataclass
from enum import Enum
from copy import deepcopy
from typing import List
import numpy as np
from algorithm_tester.mydataclasses import Task, Solution, Thing, ConfigCounter, RecursiveResult

class Context():

    def __init__(self, strategy):
        self.strategy = strategy

    def solve(self, task: Task) -> Solution:
        return self.strategy.solve(task)

class solver_strategy(object):

    def get_column_descriptions(self, show_time: bool = True):
        output = [
            "id",
            "item_count",
            "maximum_sum",
            "|",
            "items_in_bag"
        ]

        if show_time:
            # time counted as real time
            output.insert(output.index("|"), "time[ms]")
        else:
            # time counted as number of configurations
            output.insert(output.index("|"), "time[#configs]")

        return output
    
    def solve(self, task: Task) -> Solution:
        pass

class BruteForce(solver_strategy):
    """ Uses Brute force  """

    def recursive_solve(self, config_ctr: ConfigCounter, task: Task, thing_at_index: int, curr_state: RecursiveResult) -> RecursiveResult:
        config_ctr.value += 1
        curr_thing = task.things[thing_at_index]
        if thing_at_index >= task.count - 1:
            # Last thing
            if curr_thing.weight <= curr_state.remaining_capacity:
                return curr_state.new_solution(curr_thing)
            else:
                return curr_state.new_solution()
        
        # Check all possibilities
        if curr_thing.weight <= curr_state.remaining_capacity:
            # Can add current thing
            result_added = self.recursive_solve(config_ctr, task, thing_at_index + 1, curr_state.new_solution(curr_thing))
            result_not_added = self.recursive_solve(config_ctr, task, thing_at_index + 1, curr_state.new_solution())
            
            if result_added.max_value >= result_not_added.max_value:
                return result_added.new_solution()
            else:
                return result_not_added.new_solution()
        
        return self.recursive_solve(config_ctr, task, thing_at_index + 1, curr_state.new_solution())
    
    def solve(self, task: Task) -> Solution:
        # Sort things by cost/weight comparison
        task.things = sorted(task.things, key=lambda thing: thing.cost/thing.weight, reverse=True)

        config_ctr = ConfigCounter(0)
        result = self.recursive_solve(config_ctr, task, 0, RecursiveResult(task.capacity, 0, [0 for i in task.things]))

        return Solution(id=task.id, count=task.count, max_value=result.max_value, 
            elapsed_configs=config_ctr.value, things=result.things)

class BranchBound(solver_strategy):
    """ Uses BranchBound algorithm. """

    def get_max_sum(self, task: Task) -> int:
        currSum = 0
        for thing in reversed(task.things):
            currSum += thing.cost

        return currSum
    
    # maximum_sum: A sum of all objects that are after the current object
    def recursive_solve(self, config_ctr: ConfigCounter, task: Task, maximum_sum: int, thing_at_index: int, curr_state: RecursiveResult) -> RecursiveResult:
        config_ctr.value += 1
        curr_thing = task.things[thing_at_index]
        if thing_at_index >= task.count - 1:
            # Last thing
            if curr_thing.weight <= curr_state.remaining_capacity:
                return curr_state.new_solution(curr_thing)
            else:
                return curr_state.new_solution()
        
        # Check all possibilities
        if curr_thing.weight <= curr_state.remaining_capacity:
            # The subtree has high enough value, need to check if things can fit
            result_added = self.recursive_solve(config_ctr, task, maximum_sum - curr_thing.cost, thing_at_index + 1, curr_state.new_solution(curr_thing))
            
            if result_added.max_value >= curr_state.max_value + maximum_sum - curr_thing.cost:
                # The max_value of the entire branch where this item was not added is not high enough
                # so we do not need to check it
                return result_added
            
            # The subtree has high enough value, need to check if things can fit
            result_not_added = self.recursive_solve(config_ctr, task, maximum_sum - curr_thing.cost, thing_at_index + 1, curr_state.new_solution())
            
            if result_added.max_value >= result_not_added.max_value:
                return result_added.new_solution()
            else:
                return result_not_added.new_solution()

        # Current thing too heavy. The subtree has high enough value, need to check if items fit
        return self.recursive_solve(config_ctr, task, maximum_sum - curr_thing.cost, thing_at_index + 1, curr_state.new_solution())
    
    def solve(self, task: Task) -> Solution:
        # Sort things by cost/weight comparison
        task.things = sorted(task.things, key=lambda thing: thing.cost/thing.weight, reverse=True)

        # Create a descending list of maximum sums that is going to be used for value-based decisions in BranchBound alg.
        maximum_sum = self.get_max_sum(task)
        config_ctr = ConfigCounter(0)
        result = self.recursive_solve(config_ctr, task, maximum_sum, 0, RecursiveResult(task.capacity, 0, [0 for i in task.things]))

        return Solution(id=task.id, count=task.count, max_value=result.max_value, 
            elapsed_configs=config_ctr.value, things=result.things)

class UnsortedBranchBound(solver_strategy):
    """ Uses BranchBound algorithm without sorting the input first. """
    
    def solve(self, task: Task) -> Solution:
        solver = Strategies.BB.value

        # Create a descending list of maximum sums that is going to be used for value-based decisions in BranchBound alg.
        maximum_sum = solver.get_max_sum(task)
        config_ctr = ConfigCounter(0)
        result = solver.recursive_solve(config_ctr, task, maximum_sum, 0, RecursiveResult(task.capacity, 0, [0 for i in task.things]))

        return Solution(id=task.id, count=task.count, max_value=result.max_value, 
            elapsed_configs=config_ctr.value, things=result.things)

class DynamicProgramming_Weight(solver_strategy):
    """ 
    Uses DynamicProgramming iterative algorithm. 

    The DP table is a 2D table. Number of rows == capacity. 
    Each row is a list with exactly (number_of_items + 1) members.

    Algorithm fills the table from the bottom up.

    """

    def get_solution(self, task: Task, config_ctr: ConfigCounter):
        # Get the best possible value
        for i in range(1, task.count+1): 
            for w in range(1, task.capacity+1):
                config_ctr.value += 1
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

        return Solution(id=task.id, count=task.count, max_value=best_value, 
            elapsed_configs=config_ctr.value, things=tuple(output_things))

    def prepare_table(self, task: Task):
        dummy_row = [None for i in range(task.capacity + 1)]
        dummy_row[0] = 0

        self.dp_table = [[0 for i in range(task.capacity + 1)]]
        self.dp_table.extend([deepcopy(dummy_row) for i in range(task.count)])

    def solve(self, task: Task) -> Solution:
        self.prepare_table(task)

        config_ctr = ConfigCounter(0)
        return self.get_solution(task, config_ctr)

class DynamicProgramming(solver_strategy):
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

        # The infinite value == (sum of all weights + 1)
        self.max_cost_sum, max_weight_sum = self.get_max_values() 
        self.infinite_value = max(task.capacity, max_weight_sum) + 1
        
        # Create dp_table
        self.dp_table = np.zeros((self.max_cost_sum + 1, self.work_count + 1))
        self.dp_table[:,0] = self.infinite_value
        self.dp_table[0,0] = 0

        return True

    def construct_solution(self, task: Task, found_sum: int, found_weight: int, config_ctr: int) -> Solution:
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

        return Solution(id=task.id, count=task.count, max_value=found_sum, 
            relative_mistake=task.relative_mistake, elapsed_configs=config_ctr, things=tuple(things))

    def solve(self, task: Task) -> Solution:        
        self.work_count = task.count
        self.work_things = [Thing(thing.position, thing.weight, thing.cost) for thing in task.things]
        
        if not self.prepare_table(task):
            # No item can be added to the bag
            return Solution(id=task.id, count=task.count, max_value=0, relative_mistake=task.relative_mistake, things=tuple(0 for _ in range(task.count)))
        
        best_sum = 0
        config_ctr: int = 0
        for curr_sum in range(1, self.max_cost_sum + 1):
            for i in range(1, self.work_count + 1):
                config_ctr += 1
                result1, result2 = self.dp_table[curr_sum][i - 1], self.infinite_value
                curr_thing: Thing = self.work_things[i - 1]
                if curr_sum - curr_thing.cost >= 0:
                    result2 = self.dp_table[curr_sum - curr_thing.cost][i - 1] + curr_thing.weight

                self.dp_table[curr_sum][i] = min(result1, result2)
            
            if self.dp_table[curr_sum][i] <= task.capacity:
                best_sum = curr_sum

        return self.construct_solution(task=task, found_sum=best_sum, 
            found_weight=self.dp_table[best_sum][self.work_count], config_ctr=config_ctr)

class Greedy(solver_strategy):
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
        config_ctr: int = 0
        for thing in task.things:
            if thing.weight <= remaining_capacity:
                config_ctr += 1
                remaining_capacity -= thing.weight
                max_sum += thing.cost
                output_things[thing.position] = 1

            if remaining_capacity <= 0:
                break
            print

        return Solution(id=task.id, count=task.count, max_value=max_sum, 
            elapsed_configs=config_ctr, things=tuple(output_things))

class Strategies(Enum):
    Brute = BruteForce()
    BB = BranchBound()
    UBB = UnsortedBranchBound()
    DP = DynamicProgramming()
    DPWeight = DynamicProgramming_Weight()
    Greedy = Greedy()