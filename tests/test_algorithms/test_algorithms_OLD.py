# import pytest
# from flexmock import flexmock
# from click.testing import CliRunner
# from typing import List
# from algorithm_tester_common.tester_dataclasses import Algorithm, Parser, AlgTesterContext
# from algorithm_tester.tester_logic import get_instance_file_results
# from algorithm_tester.helpers import FilePair, get_input_files
# from algorithm_tester.plugins import plugins

# @pytest.mark.parametrize(
#     ['algorithm', 'exact', 'relative_mistake'],
#     [
#         ("Brute", True, None),
#         ("BB", True, None),
#         ("SBB", True, None),
#         ("DP", True, None),
#         ("DPWeight", True, None),
#         ("Greedy", False, None)
#     ]
# )
# def test_base_algorithms(algorithm: str, exact: bool, relative_mistake: float):
#     path = './data'
#     dataFiles = get_input_files(f'{path}/NK/instances')[0:2]
#     algorithm: Algorithm = plugins.get_algorithm(algorithm)

#     parser: Parser = plugins.get_parser(plugins.get_parser_names()[0])

#     context = flexmock(
#         time_retries=1,
#         check_time=False,
#         extra_options=dict()
#     )

#     for filepair in dataFiles:
#         # Get all solutions of the current problem
#         with open(filepair.solutionFile, "r") as solutionFile:
#             solutions: List[str] = solutionFile.readlines()

#         with open(filepair.dataFile, "r") as datafile:
#             it = get_instance_file_results(context=context, algorithm_name=algorithm.get_name(), parser=parser)

#             # Compare solutions
#             for index, found_solution in enumerate(it):
#                 given_solution = solutions[index].split(" ")
#                 max_value: int = found_solution.get("found_value")

#                 assert max_value is not None
#                 assert found_solution["elapsed_configs"] >= 0

#                 if exact:
#                     # Check if found value matches exactly
#                     assert int(given_solution[2]) == max_value
#                 else:
#                     # Check if the found value is at most the best value
#                     assert int(given_solution[2]) >= max_value
#                 print

#     print

# def test_sa():
#     path = './data'
#     dataFiles = get_input_files(f'{path}/NK')[0:3]

#     parser: Parser = plugins.get_parser(plugins.get_parser_names()[0])

#     extra_options = {
#             "init_temperature": 100.0,
#             "min_temperature": 1.0,
#             "cycles": 50,
#             "cooling": 0.99
#         }
    
#     context = flexmock(
#         time_retries=1,
#         output_dir="",
#         check_time=False,
#         extra_options=extra_options,
#         get_options=lambda: extra_options
#     )

#     for filepair in dataFiles:
#         # Get all solutions of the current problem
#         with open(filepair.solutionFile, "r") as solutionFile:
#             solutions: List[str] = solutionFile.readlines()

#         with open(filepair.dataFile, "r") as datafile:
#             it = get_instance_file_results(context=context, algorithm_name="SA", parser=parser)

#             # Compare solutions
#             for index, found_solution in enumerate(it):
#                 given_solution = solutions[index].split(" ")
#                 max_value: int = found_solution.get("found_value")

#                 assert max_value is not None
#                 assert found_solution["elapsed_configs"] >= 0

                
#                 # Check if the found value is at most the best value
#                 assert int(given_solution[2]) >= max_value
#                 print

#     print