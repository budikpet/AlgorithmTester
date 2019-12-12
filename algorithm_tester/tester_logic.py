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

def create_columns_description_file(algorithm: str, check_time: bool, output_dir: str):
    column_descriptions = plugins.get_algorithm(name=algorithm).get_additional_columns(check_time)

    with open(f'{output_dir}/column_description_{algorithm}.dat', "w") as f:
        f.write(f'{" ".join(column_descriptions)}\n')

def write_solution(output_file, parsed_data: Dict[str, object]):
    # output_file.write(f"{solution.output_str()}\n")
    output: str = f'{parsed_data["id"]} {parsed_data["item_count"]} {parsed_data["max_value"]} {parsed_data["algorithm_name"]} {parsed_data["elapsed_configs"]} | {" ".join(map(str, parsed_data["things"]))}'
    output_file.write(f'{output}\n')

def get_instance_file_results(context: TesterContext, datafile, algorithm_name: str):
    data = datafile.readline()
    algorithm: Algorithm = plugins.get_algorithm(algorithm_name)

    while data:
        solution: Dict[str, object] = None
        values = data.split(" ")
        id, count, capacity = int(values.pop(0)), int(values.pop(0)), int(values.pop(0))
        it = iter(values)
        things = [(pos, int(weight), int(cost)) for pos, (weight, cost) in enumerate(list(zip(it, it)))]

        parsed_data = {
            "id": id,
            "algorithm_name": algorithm_name,
            "item_count": count,
            "capacity": capacity,
            "things": things,
            "elapsed_time": 0.0
        }
        
        if context.other_options is not None:
            parsed_data.update(context.other_options)

        if context.check_time:
            # Use timeit to get time
            t = timeit.Timer(lambda: algorithm.perform_algorithm(parsed_data))
            elapsed_time, solution = t.timeit(number=time_retries)
            solution["elapsed_time"] = round((elapsed_time*1000)/time_retries, 10)   # Store in millis
        else:
            solution = algorithm.perform_algorithm(parsed_data)

        yield solution

        data = datafile.readline()
    
    print

def run_algorithms_for_file(context: TesterContext, input_file):

    for algorithm_name in context.algorithm_names:
        input_file.seek(0)
        create_columns_description_file(algorithm_name, context.check_time, context.output_dir)

        suffix = f"_{algorithm_name}"

        output_file_name = input_file.name.split("/")[-1].replace(".dat", f'{suffix}.dat')
        
        it = get_instance_file_results(context=context, datafile=input_file, algorithm_name=algorithm_name)

        print(f'Running output for: {output_file_name}. Started {time.strftime("%H:%M:%S %d.%m.")}')
        with open(f'{context.output_dir}/{output_file_name}', "w") as output_file:
            for solution in it:
                # FIXME: Parse solution dict
                write_solution(output_file, solution)
                output_file.flush()