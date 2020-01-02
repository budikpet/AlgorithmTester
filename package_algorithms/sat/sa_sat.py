from typing import List, Dict
from dataclasses import dataclass
import numpy as np
import random
from math import exp
from algorithm_tester_common.tester_dataclasses import Algorithm, AlgTesterContext, DynamicClickOption
from package_algorithms.sat.alg_dataclasses import TaskSAT

class SolutionSA:
    print

class SimulatedAnnealing_SAT(Algorithm):
    """ 
    Version of SA algorithm that is not optimized using Cython.
    
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
        return "SA_SAT"

    def get_columns(self, show_time: bool = True) -> List[str]:
        columns: List[str] = [
            "output_filename",
            "found_value",
            "vars_output",      # numbers [1..number_of_vars], negative if result is negated
            "elapsed_configs",
            "elapsed_time"
        ]

        return columns

    def get_fitness(self, task: TaskSAT, solution: SolutionSA):
        # TODO: If res = 0, then use (solution.sum_value - task.sum_of_all_values)
        # TODO: If res = 1, then use (solution.sum_value)
        return solution.sum_cost

    def initial_solution(self, task: TaskSAT) -> SolutionSA:
        solution: np.ndarray = np.zeros((task.count), dtype=int)
        sum_value = 0

        # Find solution
        # TODO Use random solution

        return SolutionSA(solution, sum_value)

    def get_new_neighbour(self, task: TaskSAT, neighbour: SolutionSA):
        index: int = random.randint(0, task.count-1)
        curr_thing: Thing = task.things[index]

        new_value: int = (neighbour[index] + 1) % 2
        neighbour[index] = new_value

        if new_value == 1:
            neighbour.sum_cost += curr_thing.cost
            neighbour.sum_weight += curr_thing.weight
            self.repair_solution(task, neighbour)
        else:
            neighbour.sum_cost -= curr_thing.cost
            neighbour.sum_weight -= curr_thing.weight

    def get_solution(self, task: TaskSAT) -> (SolutionSA, int):
        curr_temp: float = task.init_temp
        sol_cntr: int = 0

        best_sol: SolutionSA = self.initial_solution(task)
        best_fitness: float = self.get_fitness(task, best_sol)
        neighbour_sol: SolutionSA = SolutionSA(best_sol.solution.copy(), best_sol.sum_cost, best_sol.sum_weight)

        random.seed(20191219)

        while curr_temp > task.min_temp:
            for _ in range(task.cycles):
                sol_cntr += 1

                # Try neighbour solution
                self.get_new_neighbour(task, neighbour_sol)
                neighbour_fitness: float = self.get_fitness(task, neighbour_sol)

                if neighbour_fitness > best_fitness:
                    # Neighbour solution is better, accept it
                    best_fitness = neighbour_fitness
                    best_sol.copy(neighbour_sol)

                elif exp( (neighbour_fitness - best_fitness) / curr_temp) >= random.random():
                    # Simulated Annealing condition. 
                    # Enables us to accept worse solution with a certain probability
                    best_fitness = neighbour_fitness
                    best_sol.copy(neighbour_sol)

                else:
                    # Change the solution back
                    neighbour_sol.copy(neighbour_sol)
                print

            curr_temp *= task.cooling_coefficient

        return best_sol, sol_cntr
 
    def perform_algorithm(self, context: AlgTesterContext, parsed_data: Dict[str, object]) -> Dict[str, object]:
        task: TaskSAT = TaskSAT(context, parsed_data=parsed_data)
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