from typing import List, Dict
from dataclasses import dataclass
import numpy as np
from math import exp
import csa
from algorithm_tester.tester_dataclasses import Algorithm, DynamicClickOption
from package_algorithms.alg_dataclasses import Thing, TaskSA, SolutionSA

class SimulatedAnnealing(Algorithm):
    """ 
    
    Uses Simulated annealing algorithm. 
    It's a hill climbing algorithm which can accept a worse solution with a certain probability.
    It always accepts better solution if available.
    This probability depends on the size of difference between solutions and current temperature.
    The higher the temperature the more likely the algorithm is to accept a worse solution.

    Dealing with impossible solutions:
        This version uses a repair function to fix solutions whose weight is heigher than capacity.
    
    """

    def required_click_params(self) -> List[DynamicClickOption]:
        init_temp = DynamicClickOption(name="init_temperature", data_type=float, short_opt="", long_opt="--init-temperature", 
            required=True, doc_help="A float number from interval (0; +inf). Represents the starting temperature of SA.")
        cooling = DynamicClickOption(name="cooling", data_type=float, short_opt="", long_opt="--cooling", 
            required=True, doc_help="A float number from interval (0; 1]. Represents the cooling coefficient of SA. Usage: temperature1 = temperature0 * cooling")
        min_temp = DynamicClickOption(name="min_temperature", data_type=float, short_opt="", long_opt="--min-temperature", 
            required=True, doc_help="A float number from interval (0; +inf). Represents the minimum temperature of SA. The algorithm ends when this or lower temperature is achieved.")
        cycles = DynamicClickOption(name="cycles", data_type=int, short_opt="", long_opt="--cycles", 
            required=True, doc_help="An int number from interval (0; +inf). Represents the number of internal cycles of SA that are done before cooling occurs.")
        
        return [init_temp, cooling, min_temp, cycles]

    def get_name(self) -> str:
        return "SA"

    def get_columns(self, show_time: bool = True) -> List[str]:
        columns: List[str] = [
            "id",
            "item_count",
            "algorithm_name",
            "init_temperature",
            "cooling",
            "min_temperature",
            "cycles",
            "found_value",
            "elapsed_configs",
            "elapsed_time",
            "things"
        ]

        return columns

    def initial_solution(self, task: TaskSA, costs: np.ndarray, weights: np.ndarray) -> SolutionSA:
        solution: np.ndarray = np.zeros((task.count), dtype=int)
        remaining_capacity = task.capacity

        # Find solution
        weight_sum, cost_sum = 0, 0
        for index in range(task.count):
            curr_weight = weights[index]
            if curr_weight <= remaining_capacity:
                remaining_capacity -= curr_weight
                solution[index] = 1
                weight_sum += curr_weight
                cost_sum += costs[index]

            if remaining_capacity <= 0:
                break

        return SolutionSA(solution, sum_cost=cost_sum, sum_weight=weight_sum)

    def get_solution(self, task: TaskSA) -> (SolutionSA, int):
        sol_cntr: int = 0

        # Prepare things in numpy arrays only
        costs: np.ndarray = np.zeros(task.count, dtype=int)
        weights: np.ndarray = np.zeros(task.count, dtype=int)

        for (index, thing) in enumerate(task.things):
            costs[index] = thing.cost
            weights[index] = thing.weight

        # Prepare solutions

        best_sol: SolutionSA = self.initial_solution(task, costs, weights)

        best_sol.sum_cost, best_sol.sum_weight, sol_cntr = csa.get_solution(best_sol.solution, 
            best_sol.sum_cost, best_sol.sum_weight, 
            task.init_temp, task.min_temp, task.cooling_coefficient, task.cycles, task.capacity, 
            costs, weights)

        return best_sol, sol_cntr
 
    def perform_algorithm(self, parsed_data: Dict[str, object]) -> Dict[str, object]:
        task: TaskSA = TaskSA(parsed_data=parsed_data)
        task.things = sorted(task.things, key=lambda thing: thing.cost/(thing.weight + 1), reverse=True)
        
        solution, solution_cntr = self.get_solution(task)

        # Pass solution
        out_things: np.ndarray = np.zeros((task.count), dtype=int)
        for index, value in enumerate(solution.solution):
            if value == 1:
                thing: Thing = task.things[index]
                out_things[thing.position] = 1

        parsed_data.update({
            "found_value": solution.sum_cost,
            "elapsed_configs": solution_cntr,
            "things": out_things
        })

        return parsed_data