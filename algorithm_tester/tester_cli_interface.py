from subprocess import Popen, PIPE, STDOUT
import click
from typing import Dict, List
import os
import time
from algorithm_tester.plugins import plugins
from algorithm_tester.helpers import get_files_dict, create_path
from algorithm_tester.tester_logic import get_instance_file_results
from algorithm_tester.decorators import docstring_parameters

class PythonLiteralOption(click.Option):

    def type_cast_value(self, ctx, value: str):
        try:
            values = [c.strip() for c in value.split(",")]
            for out_value in values:
                if out_value not in plugins.get_algorithm_names():
                    raise click.BadParameter(value)

            return values
        except:
            raise click.BadParameter(value)

def create_columns_description_file(algorithm: str, check_time: bool, output_dir: str):
    column_descriptions = plugins.get_algorithm(name=algorithm).get_column_descriptions(check_time)

    with open(f'{output_dir}/column_description_{algorithm}.dat', "w") as f:
        f.write(f'{" ".join(column_descriptions)}\n')

def write_solution(output_file, parsed_data: Dict[str, object]):
    # output_file.write(f"{solution.output_str()}\n")
    output: str = f'{parsed_data["id"]} {parsed_data["count"]} {parsed_data["max_value"]} {parsed_data["algorithm"]} {parsed_data["elapsed_configs"]} | {" ".join(map(str, parsed_data["things"]))}'
    output_file.write(f'{output}\n')

def run_algorithms_for_file(algorithms: List[str], relative_mistake: float, check_time: bool, time_retries: int, input_file, output_dir):
    create_path(output_dir)

    for algorithm in algorithms:
        input_file.seek(0)
        create_columns_description_file(algorithm, check_time, output_dir)

        suffix = f"_{algorithm}"

        if relative_mistake is not None:
            suffix = f"{suffix}_{str(relative_mistake).replace('.', ',')}"

        output_file_name = input_file.name.split("/")[-1].replace(".dat", f'{suffix}.dat')
        
        it = get_instance_file_results(datafile=input_file, check_time=check_time, 
            algorithm=algorithm, time_retries=time_retries, relative_mistake=relative_mistake)

        print(f'Running output for: {output_file_name}. Started {time.strftime("%H:%M:%S %d.%m.")}')
        with open(f'{output_dir}/{output_file_name}', "w") as output_file:
            for solution in it:
                # FIXME: Parse solution dict
                write_solution(output_file, solution)
                output_file.flush()

@click.command()
@click.option("-s", "--algorithms", cls=PythonLiteralOption, required=True, default=",".join(plugins.get_algorithm_names()), show_default=True, help="CSV string of names of available algorithms.")
@click.option("-e", "--relative-mistake", type=float, required=False, help="Useful only for FPTAS. A float number from interval (0; 100]. Represents highest possible mistake in percents.")
@click.option("--check-time", type=bool, default=False, help="Should the result also check elapsed time.")
@click.option("--time-retries", type=int, default=5, help="How many times should we retry if elapsed time is checked.")
@click.option("-p", "--parser", type=str, show_default=True, required=True, default="KnapsackBaseParser", help="Name of the parser that is used to parse input files.")
@click.option("-c", "--communicators", type=str, required=False, help="CSV string of names of available communication interfaces.")
@click.option("-n", "--max-num", type=int, required=False, help="If set then the run_tester uses only (0, max-num] of input files.")
@click.argument("input-dir", required=True)
@click.argument("output-dir", required=True)
@docstring_parameters("Parametric docstring", "very nice!")
def run_tester(algorithms: List[str], relative_mistake: float, check_time: bool, time_retries: int, parser: str, communicators: List[str], max_num: int, input_dir, output_dir):
    """

    {} is {}.
    """
    
    files_dict = get_files_dict(input_dir)

    for key, path in files_dict.items():
        files_dict[key] = [path for path in files_dict[key] if "_inst" in path][0]

    for index, n_key in enumerate(sorted(files_dict)):
        if max_num is not None:
            if index >= max_num:
                break

        with open(files_dict[n_key], "r") as input_file:
            run_algorithms_for_file(algorithms, relative_mistake, check_time, time_retries, input_file, output_dir)

def main(prog_name: str):
    run_tester(prog_name=prog_name)   # pylint: disable=no-value-for-parameter,unexpected-keyword-arg