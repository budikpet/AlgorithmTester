from typing import List, Dict
import numpy as np
from algorithm_tester_common.tester_dataclasses import Algorithm, AlgTesterContext
from package_algorithms.alg_dataclasses import ConfigCounter, TaskKnapsackProblem, Thing, RecursiveResult, Solution, base_columns

class DynamicProgramming_Weight(Algorithm):
    """ 
    Uses DynamicProgramming iterative algorithm. 

    The DP table is a 2D table. Number of rows == capacity. 
    Each row is a list with exactly (number_of_items + 1) members.

    Algorithm fills the table from the bottom up.

    """

    def get_name(self) -> str:
        return "DPWeight"

    def get_columns(self, show_time: bool = True) -> List[str]:
        return base_columns

    def get_solution(self, task: TaskKnapsackProblem, parsed_data: Dict[str, object], config_ctr: ConfigCounter):
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
        # output_things = [0 for i in range(task.count)]
        output_things = np.zeros((task.count), dtype=int)
        
        for i in reversed(range(task.count)):
            row = self.dp_table[i]
            
            if remaining_value not in row:
                # The remaining_value is not present in i-th row so it came with i-th item
                thing: Thing = task.things[i]
                remaining_value -= thing.cost
                output_things[thing.position] = 1

            if remaining_value == 0:
                break
        
        parsed_data.update({
            "found_value": best_value,
            "elapsed_configs": config_ctr.value,
            "things": output_things
        })

        return parsed_data

    def prepare_table(self, task: TaskKnapsackProblem):
        self.dp_table = np.zeros((task.count + 1, task.capacity + 1), dtype=int)

    def perform_algorithm(self, context: AlgTesterContext, parsed_data: Dict[str, object]) -> Dict[str, object]:
        task: TaskKnapsackProblem = TaskKnapsackProblem(parsed_data=parsed_data)
        self.prepare_table(task)

        config_ctr = ConfigCounter(0)
        return self.get_solution(task, parsed_data, config_ctr)

class DynamicProgramming(Algorithm):
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

    def get_name(self) -> str:
        return "DP"

    def get_columns(self, show_time: bool = True) -> List[str]:
        return base_columns

    def simplify_task(self, task: TaskKnapsackProblem) -> bool:
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

    def prepare_table(self, task: TaskKnapsackProblem) -> bool:
        """ Prepare the DP table & other important values """

        # The infinite value == (sum of all weights + 1)
        self.max_cost_sum, max_weight_sum = self.get_max_values() 
        self.infinite_value = max(task.capacity, max_weight_sum) + 1
        
        # Create dp_table
        self.dp_table = np.zeros((self.max_cost_sum + 1, self.work_count + 1))
        self.dp_table[:,0] = self.infinite_value
        self.dp_table[0,0] = 0

        return True

    def construct_solution(self, task: TaskKnapsackProblem, parsed_data: Dict[str, object], found_sum: int, found_weight: int, config_ctr: int) -> Dict[str, object]:
        """ Reconstructs vector of things using the filled table. """

        output_things = np.zeros((task.count), dtype=int)
        curr_sum = found_sum
        curr_weight = found_weight
        for row_index in reversed(range(1, self.work_count + 1)):
            if self.dp_table[curr_sum][row_index] != self.dp_table[curr_sum][row_index - 1]:
                # Thing at row_index is in the bag
                curr_thing: Thing = self.work_things[row_index - 1]
                output_things[curr_thing.position] = 1
                curr_weight -= curr_thing.weight
                curr_sum -= curr_thing.cost

            if curr_weight == 0:
                break

        parsed_data.update({
            "found_value": found_sum,
            "elapsed_configs": config_ctr,
            "things": output_things
        })

        return parsed_data

    def perform_algorithm(self, context: AlgTesterContext, parsed_data: Dict[str, object]) -> Dict[str, object]:
        task: TaskKnapsackProblem = TaskKnapsackProblem(parsed_data=parsed_data) 
        self.work_count = task.count
        self.work_things = [Thing(thing.position, thing.weight, thing.cost) for thing in task.things]
        
        if not self.prepare_table(task):
            # No item can be added to the bag
            parsed_data.update({
                "found_value": 0,
                "elapsed_configs": 0,
                "things": np.zeros((task.count), dtype=int)
            })

            return parsed_data
        
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

        return self.construct_solution(task=task, parsed_data=parsed_data, found_sum=best_sum, 
            found_weight=self.dp_table[best_sum][self.work_count], config_ctr=config_ctr)