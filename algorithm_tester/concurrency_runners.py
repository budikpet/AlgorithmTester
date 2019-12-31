import os
import timeit
import time
import multiprocessing
import concurrent.futures
from typing import IO, Dict
from algorithm_tester.tester_dataclasses import AlgTesterContext, Algorithm, Parser
from algorithm_tester.plugins import plugins


new_template = """
def inner(_it, _timer{init}):
    {setup}
    _t0 = _timer()
    for _i in _it:
        ret_val = {stmt}
    _t1 = _timer()
    return _t1 - _t0, ret_val
"""
timeit.template = new_template

def get_click_options(context: AlgTesterContext, algorithm: Algorithm) -> Dict[str, object]:
    click_options: Dict[str, object] = context.get_options()
    click_options["algorithm_name"] = algorithm.get_name()
    click_options["algorithm"] = algorithm

    return click_options

def create_columns_description_file(context: AlgTesterContext, algorithm: Algorithm):
    """
    Create an output file with names of columns for a specific algorithm.
    
    Args:
        algorithm (str): Name of the algorithm whose columns are persisted.
        output_dir (str): Output directory.
    """
    column_descriptions = algorithm.get_columns()

    with open(f'{context.output_dir}/column_description_{algorithm.get_name()}.dat', "w") as f:
        f.write(f'{" ".join(column_descriptions)}\n')


def get_solution_for_instance(context: AlgTesterContext, algorithm: Algorithm, parsed_instance_data: Dict[str, object]) -> Dict[str, object]:
    if context.check_time:
        # Use timeit to get time
        t = timeit.Timer(lambda: algorithm.perform_algorithm(context, parsed_instance_data))
        elapsed_time, solution = t.timeit(number=context.time_retries)
        solution["elapsed_time"] = round((elapsed_time*1000)/context.time_retries, 10)   # Store in millis
    else:
        solution = algorithm.perform_algorithm(context, parsed_instance_data)

    return solution

def get_parsed_instances_data(context: AlgTesterContext, input_file: IO, parser: Parser, algorithm: Algorithm):
    parsed_instance_data = parser.get_next_instance(input_file)
    
    click_options: Dict[str, object] = get_click_options(context, algorithm)
    
    output_file_name: str = parser.get_output_file_name(context, input_file, click_options)

    while parsed_instance_data is not None:
        parsed_instance_data["output_file_name"] = output_file_name
        parsed_instance_data["algorithm_name"] = algorithm.get_name()
        parsed_instance_data["algorithm"] = algorithm
        parsed_instance_data.update(context.extra_options)

        yield parsed_instance_data

        parsed_instance_data = parser.get_next_instance(input_file)

def run_tester_for_file(context: AlgTesterContext, input_file_path: str):
    parser: Parser = plugins.get_parser(context.parser_name)
    
    print(f'Currently testing file \'{input_file_path.split("/")[-1]}\'. Started {time.strftime("%H:%M:%S %d.%m.")}')
    with open(input_file_path, "r") as input_file:
        for algorithm_name in context.algorithm_names:
            algorithm: Algorithm = plugins.get_algorithm(algorithm_name)
            
            click_options = get_click_options(context, algorithm)
            output_file_name: str = parser.get_output_file_name(context, input_file, click_options)

            create_columns_description_file(context, algorithm)
            with open(f'{context.output_dir}/{output_file_name}', "w") as output_file:

                for parsed_instance_data in get_parsed_instances_data(context, input_file, parser, algorithm):
                    solution = get_solution_for_instance(context, algorithm, parsed_instance_data)

                    parser.write_result_to_file(output_file, solution)

class BaseRunner:

    def start(self, context: AlgTesterContext, files_dict: Dict[str, str]):
        for index, n_key in enumerate(sorted(files_dict)):
            if context.max_num is not None and index >= context.max_num:
                break

            input_file_path: str = files_dict.get(n_key)
            run_tester_for_file(context, input_file_path)

            