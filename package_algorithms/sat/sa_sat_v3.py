from typing import List, Dict
from dataclasses import dataclass
import numpy as np
import random
from math import exp, ceil
from algorithm_tester_common.tester_dataclasses import Algorithm, AlgTesterContext, DynamicClickOption
from package_algorithms.sat.alg_dataclasses import TaskSAT, SolutionSA, base_columns
from package_algorithms.sat.sa_sat_v2 import SimulatedAnnealing_SAT_V2
import csa_sat

class SimulatedAnnealing_SAT_V3(SimulatedAnnealing_SAT_V2):
    """ 
    Version 3 of SA algorithm for SAT problem.
    
    Uses an improved algorithm for picking neighbour solutions. 
    If currently used solution is valid, the algorithm flips a random variable.
    If currently used solution is not valid, the algorithm finds N amount of variables that are invalid in most clauses,
    where N is in range [2, num_of_variables/5]. Then algorithm randomly flips one of these variables.
    
    """

    def get_name(self) -> str:
        return "SA_SAT_V3"

    def get_random_max_invalids_index(self, neighbour: SolutionSA) -> int:
        """
        Finds N amount of variables that are invalid in most clauses, N in range [2, num_of_variables/5].
        Then returns a random index to flip.
        
        Arguments:
            neighbour {SolutionSA} -- [description]
        
        Returns:
            int -- Random index.
        """
        num_of_maximums: int = max(ceil(neighbour.invalid_literals_per_var.size/5), 2)
        rand_index: int = random.randint(0, num_of_maximums-1)

        # Find N indexes of variables that are invalid in most clauses
        indexes = np.argpartition(neighbour.invalid_literals_per_var, -num_of_maximums)[-num_of_maximums:]
        
        return indexes[rand_index]

    def get_new_neighbour(self, task: TaskSAT, neighbour: SolutionSA):
        """
        Gets a new neighbour.

        If currently used solution is valid, the algorithm flips a random variable.
        If currently used solution is not valid, the algorithm finds N amount of variables that are invalid in most clauses,
        where N is in range [2, num_of_variables/5]. Then algorithm randomly flips one of these variables.
        
        Arguments:
            task {TaskSAT} -- [description]
            neighbour {SolutionSA} -- Currently used solution.
        """
        if neighbour.is_valid:
            index: int = random.randint(0, task.num_of_vars-1)
        else:
            # Get index of a variable that is invalid in most clauses
            index: int = self.get_random_max_invalids_index(neighbour)
        
        curr_value: int = task.weights[index]

        new_value: int = (neighbour.solution[index] + 1) % 2
        neighbour.solution[index] = new_value

        if new_value == 1:
            neighbour.sum_weight += curr_value
        else:
            neighbour.sum_weight -= curr_value

        neighbour.num_of_satisfied_clauses, neighbour.is_valid = csa_sat.check_validity(neighbour.invalid_literals_per_var, 
            task.clauses, neighbour.solution, task.num_of_clauses)

