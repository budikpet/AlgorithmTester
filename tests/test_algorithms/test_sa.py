import pytest
from flexmock import flexmock
from algorithm_tester_common.tester_dataclasses import AlgTesterContext
from package_algorithms.knapsack.sa import SimulatedAnnealing, TaskSA, SolutionSA
from package_parsers.knapsack_parser import KnapsackParser
from tests.test_algorithms.fixtures import base_context

def test_initial_solution(base_context):
    parser: KnapsackParser = KnapsackParser()
    sa: SimulatedAnnealing = SimulatedAnnealing()

    with open("tests/test_algorithms/fixtures/instance_files/NK_4_inst.dat") as input_file:
        instance = parser.get_next_instance(input_file)

    task: TaskSA = TaskSA(base_context, parsed_data=instance)
    costs, weights = sa.get_numpy_costs_weights(task)
    initial_solution: SolutionSA = sa.initial_solution(task, costs, weights)

    assert initial_solution is not None
    assert initial_solution.sum_weight < task.capacity
    assert initial_solution.solution is not None
    assert len(initial_solution.solution) == 4

    print

def test_perform_algorithm(base_context):
    fixture_path: str = "tests/test_algorithms/fixtures"
    parser: KnapsackParser = KnapsackParser()
    sa: SimulatedAnnealing = SimulatedAnnealing()

    with open(f"{fixture_path}/instance_files/NK_4_inst.dat") as input_file:
        instance = parser.get_next_instance(input_file)

    with open(f"{fixture_path}/instance_files/NK_4_sol.dat", "r") as solutionFile:
        given_solution = solutionFile.readline().split(" ")

    base_context.extra_options = {
        "init_temperature": 1000.0, "min_temperature": 1.0, "cooling": 0.99, "cycles": 20
    }

    solution = sa.perform_algorithm(base_context, instance)

    assert solution is not None
    assert solution.get("item_count") is not None
    assert solution.get("item_count") == 4
    assert solution.get("things") is not None
    assert 1 in solution.get("things")
    assert solution.get("found_value") is not None
    assert solution.get("found_value") <= int(given_solution[2])

    print