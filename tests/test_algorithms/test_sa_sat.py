import numpy as np
import pytest
import flexmock
from package_algorithms.sat.sa_sat_v1 import SimulatedAnnealing_SAT_V1
from package_algorithms.sat.alg_dataclasses import TaskSAT, SolutionSA
from tests.test_algorithms.fixtures import base_context
import csa_sat

@pytest.fixture
def base_task():
    base_task = flexmock(
        num_of_vars = 4,
        num_of_clauses = 6,
        algorithm = "SA_SAT",
        clauses = np.array([[1, 0, -3, 4], [-1, 2, -3, 0], [0, 0, 3, 4], [1, 2, -3, -4], [0, -2, 3, 0], [0, 0, -3, -4]], dtype=int),
        weights = np.array([2, 4, 1, 6], dtype=int),
        all_weights_sum = 13,

        cooling = 0.995,
        cycles = 50,
        init_temp = 1000.0,
        min_temp = 1.0,
    )

    return base_task

def set_solution_data(task, sol: SolutionSA):
    sol.num_of_satisfied_clauses, sol.is_valid = csa_sat.check_validity(sol.invalid_literals_per_var, 
        sol.invalid_literals_per_var_helper, task.clauses, sol.solution, task.num_of_clauses)

    for (index, value) in enumerate(sol.solution):
        if value == 1:
            sol.sum_weight += task.weights[index]

def test_is_solution_valid(base_context, base_task):
    alg = SimulatedAnnealing_SAT_V1()
    zero_array = np.zeros(4, dtype=int)
    
    sol1 = SolutionSA(np.array([0, 0, 0, 1], dtype=int), 0)
    sol2 = SolutionSA(np.array([1, 0, 0, 1], dtype=int), 0)
    sol3 = SolutionSA(np.array([1, 1, 1, 0], dtype=int), 0)
    sol4 = SolutionSA(np.array([0, 0, 1, 1], dtype=int), 0)

    set_solution_data(base_task, sol1)
    set_solution_data(base_task, sol2)
    set_solution_data(base_task, sol3)
    set_solution_data(base_task, sol4)

    assert sol1.is_valid
    assert sol1.num_of_satisfied_clauses == base_task.num_of_clauses
    assert (sol1.solution == np.array([0, 0, 0, 1], dtype=int)).all()
    assert (sol1.invalid_literals_per_var == np.array([0, 0, 0, 0], dtype=int)).all()

    assert sol2.is_valid
    assert sol2.num_of_satisfied_clauses == base_task.num_of_clauses
    assert (sol2.solution == np.array([1, 0, 0, 1], dtype=int)).all()
    assert (sol2.invalid_literals_per_var == np.array([0, 0, 0, 0], dtype=int)).all()

    assert sol3.is_valid
    assert sol3.num_of_satisfied_clauses == base_task.num_of_clauses
    assert (sol3.solution == np.array([1, 1, 1, 0], dtype=int)).all()
    assert (sol3.invalid_literals_per_var == np.array([0, 0, 0, 0], dtype=int)).all()

    assert not sol4.is_valid
    assert sol4.num_of_satisfied_clauses == 4
    assert (sol4.solution == np.array([0, 0, 1, 1], dtype=int)).all()
    assert (sol4.invalid_literals_per_var == np.array([1, 1, 2, 2], dtype=int)).all()

    print

def test_duplicate_solution(base_task):
    alg = SimulatedAnnealing_SAT_V1()
    
    sol = SolutionSA(np.array([0, 0, 0, 1], dtype=int), 0)
    sol.num_of_satisfied_clauses, sol.is_valid = csa_sat.check_validity(sol.invalid_literals_per_var, 
        sol.invalid_literals_per_var_helper, base_task.clauses, sol.solution, base_task.num_of_clauses)

    duplicate = alg.duplicate_solution(sol)

    assert (sol.invalid_literals_per_var == duplicate.invalid_literals_per_var).all()
    assert sol.is_valid == duplicate.is_valid
    assert sol.num_of_satisfied_clauses == duplicate.num_of_satisfied_clauses
    assert sol.sum_weight == duplicate.sum_weight

def test_is_new_sol_better(base_context, base_task):
    alg = SimulatedAnnealing_SAT_V1()
    zero_array = np.zeros(4, dtype=int)

    sol1 = SolutionSA(np.array([0, 0, 0, 1], dtype=int), 0)
    sol2 = SolutionSA(np.array([1, 0, 0, 1], dtype=int), 0)
    sol3 = SolutionSA(np.array([1, 1, 1, 0], dtype=int), 0)
    sol4 = SolutionSA(np.array([0, 0, 1, 1], dtype=int), 0)

    set_solution_data(base_task, sol1)
    set_solution_data(base_task, sol2)
    set_solution_data(base_task, sol3)
    set_solution_data(base_task, sol4)

    assert alg.is_new_sol_better(sol2, sol1)
    assert alg.is_new_sol_better(sol2, sol3)
    assert alg.is_new_sol_better(sol2, sol4)

    assert not alg.is_new_sol_better(sol4, sol1)
    assert not alg.is_new_sol_better(sol4, sol2)
    assert not alg.is_new_sol_better(sol4, sol3)