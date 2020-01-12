from typing import List, Dict
from dataclasses import dataclass
import numpy as np
import random
from math import exp
from algorithm_tester_common.tester_dataclasses import Algorithm, AlgTesterContext, DynamicClickOption
from package_algorithms.sat.alg_dataclasses import TaskSAT, SolutionSA, base_columns
import csa_sat
# TODO: Evo file
# TODO: Otestování dat, které mám
# TODO: Znovuvygenerování V1_Simple dat
# TODO: Algoritmus V4 se zvyšováním počtu kroků?
# TODO: Vypočítat i data, pro která nemám řešení? Použít odchylku vypočteného počtu splněných klauzulí od počtu všech klauzulí.

class SimulatedAnnealing_SAT_V1(Algorithm):
    """ 
    Base version of SA algorithm for SAT problem.
    
    Base working algorithm. Does not use any improving features.
    
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
        max_retry_attempts = DynamicClickOption(name="max_retry_attempts", data_type=int, short_opt="", 
            long_opt="--max-retry-attempts", required=True, 
            doc_help="An integer from interval (0; +inf). Represents the maximum number of temperature resets.")
        evo_file = DynamicClickOption(name="create_evo_file", data_type=bool, short_opt="", long_opt="--create-evo-file", 
            required=False, doc_help="If true, creates a file which contains evolution of results. Stored in output dir.")

        return [init_temp, cooling, min_temp, cycles, max_retry_attempts, evo_file]

    def get_name(self) -> str:
        return "SA_SAT_V1"

    def get_columns(self, show_time: bool = True) -> List[str]:
        return base_columns

    def duplicate_solution(self, sol: SolutionSA):
        """
        Create a deep copy of a solution.
        
        Arguments:
            sol {SolutionSA} -- Solution to copy.
        
        Returns:
            SolutionSA -- Deep copy.
        """
        duplicate: SolutionSA = SolutionSA(sol.solution.copy(), sol.sum_weight)
        np.copyto(duplicate.invalid_literals_per_var, sol.invalid_literals_per_var)
        duplicate.is_valid = sol.is_valid
        duplicate.num_of_satisfied_clauses = sol.num_of_satisfied_clauses

        return sol

    def initial_solution(self, task: TaskSAT) -> SolutionSA:
        """
        Creates initial, all zeroes solution.
        
        Arguments:
            task {TaskSAT} -- [description]
        
        Returns:
            SolutionSA -- Initial solution.
        """
        solution: SolutionSA = SolutionSA(np.zeros(task.num_of_vars, dtype=int), 0)

        solution.num_of_satisfied_clauses, solution.is_valid = csa_sat.check_validity(solution.invalid_literals_per_var, 
            solution.invalid_literals_per_var_helper, task.clauses, solution.solution, task.num_of_clauses)

        return solution

    def get_new_neighbour(self, task: TaskSAT, neighbour: SolutionSA):
        """
        Gets a new neighbour by flipping 1 random bit.
        
        Arguments:
            task {TaskSAT} -- [description]
            neighbour {SolutionSA} -- Currently used solution.
        """
        index: int = random.randint(0, task.num_of_vars-1)
        curr_value: int = task.weights[index]

        new_value: int = (neighbour.solution[index] + 1) % 2
        neighbour.solution[index] = new_value

        if new_value == 1:
            neighbour.sum_weight += curr_value
        else:
            neighbour.sum_weight -= curr_value

        neighbour.num_of_satisfied_clauses, neighbour.is_valid = csa_sat.check_validity(neighbour.invalid_literals_per_var, 
            neighbour.invalid_literals_per_var_helper, task.clauses, neighbour.solution, task.num_of_clauses)


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

    def try_new_solution(self, task: TaskSAT, best_sol: SolutionSA, curr_sol: SolutionSA, neighbour_sol: SolutionSA, curr_temp: float):
        """
        Generates neighbour solution. 
        
        Arguments:
            task {TaskSAT} -- [description]
            best_sol {SolutionSA} -- Best solution ever found.
            curr_sol {SolutionSA} -- Currently used solution.
            neighbour_sol {SolutionSA} -- Solution used to contain newly generated neighbour solution.
            curr_temp {float} -- Current temperature.
        """
        
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

    def compute_solution_with_evo(self, task: TaskSAT, best_sol: SolutionSA, curr_sol: SolutionSA, neighbour_sol: SolutionSA):
        curr_temp: float = task.init_temp
        sol_cntr: int = 0

        with open(task.evo_filepath, "w") as evo_file:
            while curr_temp > task.min_temp:
                for _ in range(task.cycles):
                    sol_cntr += 1

                    self.try_new_solution(task, best_sol, curr_sol, neighbour_sol, curr_temp)
                    evo_file.write(f'{task.sol_file_name} {curr_sol.num_of_satisfied_clauses} {curr_sol.sum_weight}\n')


                curr_temp *= task.cooling

        return best_sol, sol_cntr

    def compute_solution(self, task: TaskSAT, best_sol: SolutionSA, curr_sol: SolutionSA, neighbour_sol: SolutionSA):
        curr_temp: float = task.init_temp
        sol_cntr: int = 0

        while curr_temp > task.min_temp:
            for _ in range(task.cycles):
                sol_cntr += 1

                self.try_new_solution(task, best_sol, curr_sol, neighbour_sol, curr_temp)


            curr_temp *= task.cooling

        return best_sol, sol_cntr


    def get_solution(self, task: TaskSAT) -> (SolutionSA, int):
        """
        Compute solution.
        
        Returns:
            SolutionSA -- Found solution.
        """

        # np.random.seed(20191219)
        # random.seed(20191219)

        best_sol: SolutionSA = self.initial_solution(task)
        curr_sol: SolutionSA = self.duplicate_solution(best_sol)
        neighbour_sol: SolutionSA = self.duplicate_solution(best_sol)

        if task.evo_filepath is not None:
            return self.compute_solution_with_evo(task, best_sol, curr_sol, neighbour_sol)
        else:
            return self.compute_solution(task, best_sol, curr_sol, neighbour_sol)
 
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
            "is_valid": solution.is_valid,
            "num_of_satisfied_clauses": solution.num_of_satisfied_clauses,
            "retry_count": 1,
            "elapsed_configs": solution_cntr
        })

        return parsed_data