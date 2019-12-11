import pytest
from click.testing import CliRunner
from typing import List
from algorithm_tester.algorithms import Algorithm
from algorithm_tester.tester_logic import get_instance_file_results
from algorithm_tester.helpers import FilePair, get_files
from algorithm_tester.plugins import plugins

@pytest.mark.parametrize(
    ['algorithm', 'exact', 'relative_mistake'],
    [
        (plugins.get_algorithm("Brute"), True, None),
        (plugins.get_algorithm("BB"), True, None),
        (plugins.get_algorithm("SBB"), True, None),
        (plugins.get_algorithm("DP"), True, None),
        (plugins.get_algorithm("DPWeight"), True, None),
        (plugins.get_algorithm("Greedy"), False, None)
    ]
)
def test_algorithm(algorithm: Algorithm, exact: bool, relative_mistake: float):
    path = './data'
    dataFiles = get_files(f'{path}/NK')[0:1]

    for filepair in dataFiles:
        # Get all solutions of the current problem
        with open(filepair.solutionFile, "r") as solutionFile:
            solutions: List[str] = solutionFile.readlines()

        with open(filepair.dataFile, "r") as datafile:
            it = get_instance_file_results(datafile=datafile, algorithm=algorithm.get_name(),
                time_retries=1, check_time=False)

            # Compare solutions
            for index, solution in enumerate(it):
                given_solution = solutions[index].split(" ")
                found_solution = solution
                max_value: int = found_solution.get("max_value")

                assert max_value is not None
                assert found_solution["elapsed_configs"] >= 0

                if exact:
                    # Check if found value matches exactly
                    assert int(given_solution[2]) == max_value
                else:
                    # Check if the found value is at most the best value
                    assert int(given_solution[2]) >= max_value
                print

    print