from typing import List, Dict
from dataclasses import dataclass
import numpy as np
import random
from math import exp
from algorithm_tester.tester_dataclasses import Algorithm, DynamicClickOption
from package_algorithms.alg_dataclasses import Thing, TaskKnapsackProblem

class TaskSA(TaskKnapsackProblem):
    
    def __init__(self, parsed_data: Dict[str, object]):
        super().__init__(parsed_data)
        self.init_temp: float = parsed_data.get("init_temperature")
        self.cooling_coefficient: float = parsed_data.get("cooling")
        self.min_temp: float = parsed_data.get("min_temperature")
        self.cycles: int = parsed_data.get("cycles")


class SolutionSA():

    def __init__(self, solution: np.ndarray, cost: int, weight: int):
        self.solution = solution
        self.cost = cost
        self.weight = weight

class SimulatedAnnealing(Algorithm):
    """ 
    
    Uses Simulated annealing algorithm. 
    It's a hill climbing algorithm which can accept a worse solution with a certain probability.
    It always accepts better solution if available.
    This probability depends on the size of difference between solutions and current temperature.
    The higher the temperature the more likely the algorithm is to accept a worse solution.
    
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

    def get_sums(self, task: TaskSA, solution: np.ndarray):
        cost, weight = 0, 0

        # Get sums of weights and costs
        for (index, value) in enumerate(solution):
            if value == 1:
                curr_thing: Thing = task.things[index]
                cost += curr_thing.cost
                weight += curr_thing.weight

        return cost, weight

    def get_fitness(self, task: TaskSA, solution: np.ndarray):
        cost, weight = self.get_sums(task, solution)

        return cost

    def initial_solution(self, task: TaskSA) -> SolutionSA:
        solution: np.ndarray = np.zeros((task.count), dtype=int)
        remaining_capacity = task.capacity

        # Find solution
        weight, cost = 0, 0
        for index, thing in enumerate(task.things):
            if thing.weight <= remaining_capacity:
                remaining_capacity -= thing.weight
                solution[index] = 1
                weight += thing.weight
                cost += thing.cost

            if remaining_capacity <= 0:
                break

        return SolutionSA(solution, cost, weight)

    def repair_solution(self, task: TaskSA, solution: np.ndarray):
        print

    def get_solution(self, task: TaskSA) -> (np.ndarray, int):
        curr_temp: float = task.init_temp
        sol_cntr: int = 0

        best_sol: SolutionSA = self.initial_solution(task)
        neighbour_sol: SolutionSA = SolutionSA(best_sol.solution.copy(), cost=best_sol.cost, weight=best_sol.weight)

        random.seed(20191219)

        while curr_temp > task.min_temp:
            for _ in range(task.cycles):
                sol_cntr += 1
                index: int = random.randint(0, task.count-1)

                # Try neighbour solution
                neighbour_sol[index] = (neighbour_sol[index] + 1) % 2
                self.repair_solution(task, neighbour_sol)
                neighbour_fitness: float = self.get_fitness(task, best_sol)

                if neighbour_fitness > best_fitness:
                    # Neighbour solution is better, accept it
                    best_fitness = neighbour_fitness
                    best_sol = neighbour_sol.copy()

                elif exp( (neighbour_fitness - best_fitness) / curr_temp) >= random.random():
                    # Simulated Annealing condition. 
                    # Enables us to accept worse solution with a certain probability
                    best_fitness = neighbour_fitness
                    best_sol = neighbour_sol.copy()

                else:
                    # Change the solution back
                    neighbour_sol = best_sol.copy()
                print

            curr_temp *= task.cooling_coefficient

        return best_sol, sol_cntr
 
    def perform_algorithm(self, parsed_data: Dict[str, object]) -> Dict[str, object]:
        task: TaskSA = TaskSA(parsed_data=parsed_data)
        task.things = sorted(task.things, key=lambda thing: thing.cost/(thing.weight + 1), reverse=True)
        
        solution, solution_cntr = self.get_solution(task)

        max_cost, weight = self.get_sums(task, solution)

        parsed_data.update({
            "found_value": max_cost,
            "elapsed_configs": solution_cntr,
            "things": solution
        })

        return parsed_data