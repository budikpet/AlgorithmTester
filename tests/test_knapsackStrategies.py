import pytest
from click.testing import CliRunner
from typing import List
from algorithm_tester.knapsack_solver import knapsack_solver
from algorithm_tester.solver_strategy import Strategies
from algorithm_tester.mydataclasses import Solution
from algorithm_tester.helpers import FilePair, getFiles

@pytest.mark.parametrize(
    ['strategy', 'exact', 'relative_mistake'],
    [
        (Strategies.Brute, True, None),
        (Strategies.BB, True, None),
        (Strategies.SBB, True, None),
        (Strategies.DP, True, None),
        (Strategies.DPWeight, True, None),
        (Strategies.Greedy, False, None)
    ]
)
def test_algorithm(strategy: Strategies, exact: bool, relative_mistake: float):
    path = './data'
    dataFiles = getFiles(f'{path}/NK')[0:1]

    for filepair in dataFiles:
        # Get all solutions of the current problem
        with open(filepair.solutionFile, "r") as solutionFile:
            solutions: List[str] = solutionFile.readlines()

        with open(filepair.dataFile, "r") as datafile:
            it = knapsack_solver(datafile=datafile, strategy=strategy.name, 
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