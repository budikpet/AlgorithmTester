from typing import List, Dict
import numpy as np
from algorithm_tester.tester_dataclasses import Algorithm, AlgTesterContext
from package_algorithms.alg_dataclasses import ConfigCounter, TaskKnapsackProblem, Thing, RecursiveResult, Solution, base_columns

class BranchBound(Algorithm):
    """ Uses BranchBound algorithm. """

    def get_name(self) -> str:
        return "BB"

    def get_columns(self, show_time: bool = True) -> List[str]:
        return base_columns

    def get_max_sum(self, task: TaskKnapsackProblem) -> int:
        currSum = 0
        for thing in reversed(task.things):
            currSum += thing.cost

        return currSum
    
    # maximum_sum: A sum of all objects that are after the current object
    def recursive_solve(self, config_ctr: ConfigCounter, task: TaskKnapsackProblem, maximum_sum: int, thing_at_index: int, curr_state: RecursiveResult) -> RecursiveResult:
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
    
    def perform_algorithm(self, context: AlgTesterContext, parsed_data: Dict[str, object]) -> Dict[str, object]:
        # Create a descending list of maximum sums that is going to be used for value-based decisions in BranchBound alg.
        task: TaskKnapsackProblem = TaskKnapsackProblem(parsed_data=parsed_data)
        maximum_sum = self.get_max_sum(task)
        config_ctr = ConfigCounter(0)
        things = np.zeros((task.count), dtype=int)
        result = self.recursive_solve(config_ctr, task, maximum_sum, 0, RecursiveResult(remaining_capacity=task.capacity, 
            max_value=0, things=things))

        parsed_data.update({
            "found_value": result.max_value,
            "elapsed_configs": config_ctr.value,
            "things": result.things
        })

        return parsed_data

class SortedBranchBound(Algorithm):
    """ Uses BranchBound algorithm, sorts the input first. """

    def get_name(self) -> str:
        return "SBB"

    def get_columns(self, show_time: bool = True) -> List[str]:
        return base_columns

    def perform_algorithm(self, context: AlgTesterContext, parsed_data: Dict[str, object]) -> Dict[str, object]:
        algorithm = BranchBound()

        # Sort things by cost/weight comparison
        task: TaskKnapsackProblem = TaskKnapsackProblem(parsed_data=parsed_data)
        task.things = sorted(task.things, key=lambda thing: thing.cost/thing.weight, reverse=True)

        # Create a descending list of maximum sums that is going to be used for value-based decisions in BranchBound alg.
        maximum_sum = algorithm.get_max_sum(task)
        config_ctr = ConfigCounter(0)
        things = np.zeros((task.count), dtype=int)
        result = algorithm.recursive_solve(config_ctr, task, maximum_sum, 0, RecursiveResult(remaining_capacity=task.capacity, 
            max_value=0, things=things))

        parsed_data.update({
            "found_value": result.max_value,
            "elapsed_configs": config_ctr.value,
            "things": result.things
        })

        return parsed_data
