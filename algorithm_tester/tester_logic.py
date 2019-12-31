import os
import timeit
import time
from typing import Dict, List, IO
from algorithm_tester.helpers import get_files_dict, create_path
from algorithm_tester.tester_dataclasses import AlgTesterContext, Algorithm, Parser
from algorithm_tester.plugins import plugins
from algorithm_tester.concurrency_runners import BaseRunner, ConcurrentFilesRunner, ConcurrentInstancesRunner

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

def get_instance_file_results(context: AlgTesterContext, algorithm_name: str, parser: Parser, input_file: IO) -> Dict[str, object]:
    """
    Parsed instances are passed to the provided algorithm. Results are returned one by one.
    
    Args:
        context (AlgTesterContext): Input data.
        algorithm_name (str): Name of the algorithm used to compute results.
        parser (Parser): Used parser.
    
    Yields:
        Dict[str, object]: Result data of one instance from the input file.
    """
    parsed_data = parser.get_next_instance(input_file)
    algorithm: Algorithm = plugins.get_algorithm(algorithm_name)
    
    click_options: Dict[str, object] = context.get_options()
    click_options["algorithm_name"] = algorithm_name
    click_options["algorithm"] = algorithm
    
    output_file_name: str = parser.get_output_file_name(context, input_file, click_options)

    while parsed_data is not None:
        parsed_data["output_file_name"] = output_file_name
        parsed_data["algorithm_name"] = algorithm_name
        parsed_data.update(context.extra_options)

        if context.check_time:
            # Use timeit to get time
            t = timeit.Timer(lambda: algorithm.perform_algorithm(context, parsed_data))
            elapsed_time, solution = t.timeit(number=context.time_retries)
            solution["elapsed_time"] = round((elapsed_time*1000)/context.time_retries, 10)   # Store in millis
        else:
            solution = algorithm.perform_algorithm(context, parsed_data)

        yield solution

        parsed_data = parser.get_next_instance(input_file)
    
    print

def run_algorithms_for_file(context: AlgTesterContext, input_file: IO):
    """
    Generate output files for the specified input file.

    Parses input file using the provided parser, instance data are passed to all required algorithms, results are written to output files.
    
    Args:
        context (AlgTesterContext): Input data.
        input_file ([type]): Opened input file.
    """
    parser: Parser = plugins.get_parser(name=context.parser_name)

    for algorithm_name in context.algorithm_names:
        algorithm: Algorithm = plugins.get_algorithm(algorithm_name)

        # Move reader to the start of the file
        input_file.seek(0)
        
        create_columns_description_file(algorithm_name, context.output_dir)
        
        it = get_instance_file_results(context=context, algorithm_name=algorithm_name, parser=parser, input_file=input_file)

        click_options: Dict[str, object] = context.get_options()
        click_options["algorithm_name"] = algorithm_name
        click_options["algorithm"] = algorithm

        output_file_name: str = parser.get_output_file_name(context, input_file, click_options)
        print(f'Running output for: {output_file_name}. Started {time.strftime("%H:%M:%S %d.%m.")}')
        with open(f'{context.output_dir}/{output_file_name}', "w") as output_file:
            for solution in it:
                parser.write_result_to_file(output_file, {**click_options, **solution} )
                output_file.flush()

def run_tester(algorithms: List[str], check_time: bool, time_retries: int, parser: str, communicators: List[str], max_num: int, input_dir, output_dir, extra_options):
    files_dict = get_files_dict(input_dir)

    context: AlgTesterContext = AlgTesterContext(
        algorithms=algorithms, parser=parser, communicators=communicators,
        max_num=max_num, check_time=check_time, time_retries=time_retries,
        extra_options=extra_options,
        input_dir=input_dir, output_dir=output_dir
        )

    for key, path in files_dict.items():
        files_dict[key] = [path for path in files_dict[key] if "_inst" in path][0]

    create_path(output_dir)

    runner = ConcurrentInstancesRunner()

    runner.start(context, files_dict)
    print(f'Algorithm ended at {time.strftime("%H:%M:%S %d.%m.")}')