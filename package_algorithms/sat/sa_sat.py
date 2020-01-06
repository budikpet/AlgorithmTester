from typing import List, Dict
from dataclasses import dataclass
import numpy as np
import random
from math import exp
from algorithm_tester_common.tester_dataclasses import Algorithm, AlgTesterContext, DynamicClickOption
from package_algorithms.sat.alg_dataclasses import TaskSAT, SolutionSA

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
        if solution.is_valid:
            return solution.sum_value
        else:
            return solution.sum_value - task.all_weights_sum

    def is_solution_valid(self, task: TaskSAT, solution: np.ndarray) -> bool:
        for clause in task.clauses:
            res: bool = False

            for value in clause:
                if value != 0:
                    sol_value: int = solution[abs(value) - 1]
                    if (sol_value == 0 and value < 0) or (sol_value == 1 and value > 0):
                        # This clause == 1, continue to other clauses
                        res = True
                        continue

            if res == False:
                # One clause is False, then result is false
                return False
        return True

    def initial_solution(self, task: TaskSAT) -> SolutionSA:
        # TODO: Možná vytvořit tak, aby byl validní - 
        # - seřadit si klauzule od té s nejvíce nulami (má nejméně zadaný proměnných)
        # - do pole výsledků si vkládat 1 a 0 podle toho, co daná klauzule vyžaduje
        # - bude potřeba si pamatovat, že např. proměnná 1 byla předtím v klauzuli s proměnnou 2, 3... při ukládání do výsledků
        # - na konci budou projité všechny klauzule
        solution: np.ndarray = np.random.random_integers(0, 1, size=task.num_of_vars)
        sum_value = 0

        for index, value in enumerate(solution):
            if value == 1:
                sum_value += task.weights[index]

        return SolutionSA(solution, sum_value, self.is_solution_valid(task, solution))

    def get_new_neighbour(self, task: TaskSAT, neighbour: SolutionSA):
        index: int = random.randint(0, task.num_of_vars-1)
        curr_value: int = task.weights[index]

        new_value: int = (neighbour.solution[index] + 1) % 2
        neighbour.solution[index] = new_value

        if new_value == 1:
            neighbour.sum_value += curr_value
        else:
            neighbour.sum_value -= curr_value

        neighbour.is_valid = self.is_solution_valid(task, neighbour.solution)

    def get_solution(self, task: TaskSAT) -> (SolutionSA, int):
        curr_temp: float = task.init_temp
        sol_cntr: int = 0

        np.random.seed(20191219)
        random.seed(20191219)

        best_sol: SolutionSA = self.initial_solution(task)
        best_fitness: float = self.get_fitness(task, best_sol)
        
        curr_sol: SolutionSA = SolutionSA(best_sol.solution.copy(), best_sol.sum_value, best_sol.is_valid)
        curr_fitness: float = self.get_fitness(task, curr_sol)
        
        neighbour_sol: SolutionSA = SolutionSA(curr_sol.solution.copy(), curr_sol.sum_value, curr_sol.is_valid)

        while curr_temp > task.min_temp:
            for _ in range(task.cycles):
                sol_cntr += 1

                # Try neighbour solution
                self.get_new_neighbour(task, neighbour_sol)
                neighbour_fitness: float = self.get_fitness(task, neighbour_sol)

                if neighbour_fitness > curr_fitness:
                    # Neighbour solution is better, accept it
                    curr_fitness = neighbour_fitness
                    curr_sol.copy(neighbour_sol)

                    if curr_fitness > best_fitness:
                        best_fitness = curr_fitness
                        best_sol.copy(curr_sol)

                elif exp( abs(neighbour_fitness - curr_fitness) / curr_temp) > random.random():
                    # Simulated Annealing condition. 
                    # Enables us to accept worse solution with a certain probability
                    curr_fitness = neighbour_fitness
                    curr_sol.copy(neighbour_sol)

                else:
                    # Change the solution back
                    neighbour_sol.copy(neighbour_sol)
                print

            curr_temp *= task.cooling

        return best_sol, sol_cntr
 
    def perform_algorithm(self, context: AlgTesterContext, parsed_data: Dict[str, object]) -> Dict[str, object]:
        task: TaskSAT = TaskSAT(context=context, parsed_data=parsed_data)
        
        solution, solution_cntr = self.get_solution(task)

        # Pass solution
        out_vars: np.ndarray = np.zeros(task.num_of_vars + 1, dtype=int)
        for index, value in enumerate(solution.solution):
            if value == 1:
                out_vars[index] = index
            else:
                out_vars[index] = -index

        parsed_data.update({
            "found_value": solution.sum_value,
            "vars_output": out_vars,
            "elapsed_configs": solution_cntr
        })

        return parsed_data