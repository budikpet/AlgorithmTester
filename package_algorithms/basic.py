from typing import List, Dict
import numpy as np
from algorithm_tester.algorithms import Algorithm
from package_algorithms.tester_dataclasses import ConfigCounter, Task, Thing, RecursiveResult, Solution

class BruteForce(Algorithm):
    """ Uses Brute force  """

    def get_name(self) -> str:
        return "Brute"

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
    
    def perform_algorithm(self, parsed_data: Dict[str, object]) -> Dict[str, object]:
        # Sort things by cost/weight comparison
        task: Task = Task(parsed_data=parsed_data)
        task.things = sorted(task.things, key=lambda thing: thing.cost/thing.weight, reverse=True)

        config_ctr = ConfigCounter(0)
        things = np.zeros((task.count), dtype=int)
        result = self.recursive_solve(config_ctr, task, 0, RecursiveResult(remaining_capacity=task.capacity, 
            max_value=0, things=things))

        parsed_data.update({
            "max_value": result.max_value,
            "elapsed_configs": config_ctr.value,
            "things": "tmp_result.things"
        })

        return parsed_data

class Greedy(Algorithm):
    """ 
    Uses simple Greedy heuristics. 

    Things list are sorted by key (cost/weight) in descending order. The list is iterated through and things are added to the bag
    if they fit.
    
    """

    def get_name(self) -> str:
        return "Greedy"

    def perform_algorithm(self, parsed_data: Dict[str, object]) -> Dict[str, object]:
        # Sort things by cost/weight comparison descending
        task: Task = Task(parsed_data=parsed_data)
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

        parsed_data.update({
            "max_value": max_sum,
            "elapsed_configs": config_ctr,
            "things": "tmp_output_things"
        })

        return parsed_data