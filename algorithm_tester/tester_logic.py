import os
import timeit
import click
import time
from typing import Dict, List
from algorithm_tester.tester_dataclasses import TesterContext, Algorithm, Parser
from algorithm_tester.plugins import plugins

# Enable timeit to return elapsed time and return value
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

def create_columns_description_file(algorithm: str, output_dir: str):
    """
    Create an output file with names of columns for a specific algorithm.
    
    Args:
        algorithm (str): Name of the algorithm whose columns are persisted.
        output_dir (str): Output directory.
    """
    column_descriptions = plugins.get_algorithm(name=algorithm).get_columns()

    with open(f'{output_dir}/column_description_{algorithm}.dat', "w") as f:
        f.write(f'{" ".join(column_descriptions)}\n')

def get_instance_file_results(context: TesterContext, algorithm_name: str, parser: Parser) -> Dict[str, object]:
    """
    Parsed instances are passed to the provided algorithm. Results are returned one by one.
    
    Args:
        context (TesterContext): Input data.
        algorithm_name (str): Name of the algorithm used to compute results.
        parser (Parser): Used parser.
    
    Yields:
        Dict[str, object]: Result data of one instance from the input file.
    """
    parsed_data = parser.get_next_instance()
    algorithm: Algorithm = plugins.get_algorithm(algorithm_name)

    while parsed_data is not None:
        parsed_data["algorithm_name"] = algorithm_name
        parsed_data.update(context.extra_options)

        if context.check_time:
            # Use timeit to get time
            t = timeit.Timer(lambda: algorithm.perform_algorithm(parsed_data))
            elapsed_time, solution = t.timeit(number=context.time_retries)
            solution["elapsed_time"] = round((elapsed_time*1000)/context.time_retries, 10)   # Store in millis
        else:
            solution = algorithm.perform_algorithm(parsed_data)

        yield solution

        parsed_data = parser.get_next_instance()
    
    print

def run_algorithms_for_file(context: TesterContext, input_file):
    """
    Generate output files for the specified input file.

    Parses input file using the provided parser, instance data are passed to all required algorithms, results are written to output files.
    
    Args:
        context (TesterContext): Input data.
        input_file ([type]): Opened input file.
    """
    parser: Parser = plugins.get_parser(name=context.parser_name)
    parser.set_input_file(input_file)

    for algorithm_name in context.algorithm_names:
        algorithm: Algorithm = plugins.get_algorithm(algorithm_name)
        parser.reload_input_file()
        
        create_columns_description_file(algorithm_name, context.output_dir)
        
        it = get_instance_file_results(context=context, algorithm_name=algorithm_name, parser=parser)

        click_options: Dict[str, object] = context.get_options()
        click_options["algorithm_name"] = algorithm_name
        click_options["algorithm"] = algorithm

        output_file_name: str = parser.get_output_file_name(click_options)
        print(f'Running output for: {output_file_name}. Started {time.strftime("%H:%M:%S %d.%m.")}')
        with open(f'{context.output_dir}/{output_file_name}', "w") as output_file:
            for solution in it:
                parser.write_result_to_file(output_file, {**click_options, **solution} )
                output_file.flush()