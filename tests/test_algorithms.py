import pytest
from click.testing import CliRunner
from typing import List
from algorithm_tester.tester_logic import test_instance_file
from algorithm_tester.tested_algorithms import Algorithms
from algorithm_tester.tester_dataclasses import Solution
from algorithm_tester.helpers import FilePair, get_files

@pytest.mark.parametrize(
    ['algorithm', 'exact', 'relative_mistake'],
    [
        (Algorithms.Brute, True, None),
        (Algorithms.BB, True, None),
        (Algorithms.SBB, True, None),
        (Algorithms.DP, True, None),
        (Algorithms.DPWeight, True, None),
        (Algorithms.Greedy, False, None)
    ]
)
def test_algorithm(algorithm: Algorithms, exact: bool, relative_mistake: float):
    path = './data'
    dataFiles = get_files(f'{path}/NK')[0:1]

    for filepair in dataFiles:
        # Get all solutions of the current problem
        with open(filepair.solutionFile, "r") as solutionFile:
            solutions: List[str] = solutionFile.readlines()

        with open(filepair.dataFile, "r") as datafile:
            it = test_instance_file(datafile=datafile, algorithm=algorithm.name, 
                relative_mistake=relative_mistake, time_retries=1, check_time=False)

            # Compare solutions
            for index, solution in enumerate(it):
                given_solution = solutions[index].split(" ")
                found_solution = solution.output_str().split(" ")

                assert int(found_solution[4]) >= 0
                    
                if exact:
                    # Check if found value matches exactly
                    assert int(given_solution[2]) == int(found_solution[2])
                else:
                    # Check if the found value is at most the best value
                    assert int(given_solution[2]) >= int(found_solution[2])
                print

    print