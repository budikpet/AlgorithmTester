import numpy as np
import pytest
import flexmock
from package_algorithms.sat.sa_sat import SimulatedAnnealing_SAT
from package_algorithms.sat.alg_dataclasses import TaskSAT
from tests.test_algorithms.fixtures import base_context

@pytest.fixture
def base_task():
    base_task = flexmock(
        num_of_vars = 4,
        num_of_clauses = 6,
        algorithm = "SA_SAT",
        clauses = np.array([[1, 0, -3, 4], [-1, 2, -3, 0], [0, 0, 3, 4], [1, 2, -3, -4], [0, 0, -2, 3], [0, 0, -3, -4]], dtype=int),
        weights = np.array([2, 4, 1, 6], dtype=int),
        all_weights_sum = 13,

        cooling = 0.995,
        cycles = 50,
        init_temp = 1000.0,
        min_temp = 1.0,
    )

    return base_task

def test_is_solution_valid(base_context, base_task):
    alg = SimulatedAnnealing_SAT()
    
    sol1 = np.array([0, 0, 0, 1], dtype=int)
    sol2 = np.array([1, 0, 0, 1], dtype=int)
    sol3 = np.array([1, 1, 1, 0], dtype=int)
    sol4 = np.array([0, 0, 1, 1], dtype=int)

    assert alg.is_solution_valid(base_task, sol1) == True
    assert alg.is_solution_valid(base_task, sol2) == True
    assert alg.is_solution_valid(base_task, sol3) == True
    assert alg.is_solution_valid(base_task, sol4) == False

    print