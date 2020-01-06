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

    def duplicate_solution(self, sol: SolutionSA):
        duplicate: SolutionSA = SolutionSA(sol.solution.copy(), sol.sum_weight)
        np.copyto(duplicate.invalid_literals_per_var, sol.invalid_literals_per_var)
        duplicate.is_valid = sol.is_valid
        duplicate.num_of_satisfied_clauses = sol.num_of_satisfied_clauses

        return sol

    def check_validity(self, task: TaskSAT, sol: SolutionSA):
        sol.invalid_literals_per_var[:] = 0
        sol.num_of_satisfied_clauses = 0
        sol.is_valid = False

        for clause in task.clauses:
            is_satisfied: bool = False

            for value in clause:
                if value != 0:
                    index = abs(value) - 1
                    sol_value: int = sol.solution[index]
                    if (sol_value == 0 and value < 0) or (sol_value == 1 and value > 0):
                        # Clause satisfied
                        is_satisfied = True
                    else: 
                        sol.invalid_literals_per_var[index] += 1
            
            if is_satisfied:
                # Last clause was satisfied
                sol.num_of_satisfied_clauses += 1
        
        sol.is_valid = task.num_of_clauses == sol.num_of_satisfied_clauses

    def initial_solution(self, task: TaskSAT) -> SolutionSA:
        solution: SolutionSA = SolutionSA(np.zeros(task.num_of_vars, dtype=int), 0)

        self.check_validity(task, solution)

        return solution

    def get_new_neighbour(self, task: TaskSAT, neighbour: SolutionSA):
        index: int = random.randint(0, task.num_of_vars-1)
        curr_value: int = task.weights[index]

        new_value: int = (neighbour.solution[index] + 1) % 2
        neighbour.solution[index] = new_value

        if new_value == 1:
            neighbour.sum_weight += curr_value
        else:
            neighbour.sum_weight -= curr_value

        self.check_validity(task, neighbour)

    def is_new_sol_better(self, new_sol: SolutionSA, curr_sol: SolutionSA) -> bool:
        """
        Compare new and current solution.
        
        Arguments:
            new_sol {SolutionSA} -- New neighbour solution.
            curr_sol {SolutionSA} -- Currently used solution.
        
        Returns:
            bool -- True if neighbour solution is better.
        """

        if new_sol.is_valid and curr_sol.is_valid:
            # Both valid, compare weights
            return new_sol.sum_weight > curr_sol.sum_weight

        if not new_sol.is_valid and curr_sol.is_valid:
            # Both invalid, compare number of satisfied clauses
            return new_sol.num_of_satisfied_clauses > curr_sol.num_of_satisfied_clauses

        if new_sol.is_valid and not curr_sol.is_valid:
            # Only neighbour is valid -> it is better
            return True

        # Only current solution is valid -> it is better
        return False

    def get_solution(self, task: TaskSAT) -> (SolutionSA, int):
        curr_temp: float = task.init_temp
        sol_cntr: int = 0

        np.random.seed(20191219)
        random.seed(20191219)

        best_sol: SolutionSA = self.initial_solution(task)
        curr_sol: SolutionSA = self.duplicate_solution(best_sol)
        neighbour_sol: SolutionSA = self.duplicate_solution(best_sol)

        while curr_temp > task.min_temp:
            for _ in range(task.cycles):
                sol_cntr += 1

                # Try neighbour solution
                self.get_new_neighbour(task, neighbour_sol)

                if self.is_new_sol_better(neighbour_sol, curr_sol):
                    # Neighbour solution is better, accept it
                    curr_sol.copy(neighbour_sol)

                    if self.is_new_sol_better(curr_sol, best_sol):
                        best_sol.copy(curr_sol)

                elif exp( (neighbour_sol.num_of_satisfied_clauses - curr_sol.num_of_satisfied_clauses) / curr_temp) > random.random():
                    # Simulated Annealing condition. 
                    # Enables us to accept worse solution with a certain probability
                    # Never takes the new solution if new solution is invalid and old one is valid 
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
            "found_value": solution.sum_weight,
            "vars_output": out_vars,
            "elapsed_configs": solution_cntr
        })

        return parsed_data