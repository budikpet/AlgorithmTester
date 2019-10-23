from subprocess import Popen, PIPE, STDOUT
import click
from typing import Dict
import os
import time
from solverStrategy import Strategies
from helpers import get_files_dict

def create_path(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def create_columns_description_file(strategy: str, check_time: bool, output_dir: str):
    column_descriptions = Strategies[strategy].value.get_column_descriptions(check_time)

    with open(f'{output_dir}/column_description_{strategy}.dat', "w") as f:
        f.write(f'{" ".join(column_descriptions)}\n')

@click.group()
def generate_output():
    pass

inputStrategies = [strategy.name for strategy in Strategies]

@generate_output.command()
@click.option("-s", "--strategy", type=click.Choice(inputStrategies), default=inputStrategies[0], show_default=True)
@click.option("-e", "--relative-mistake", type=float, required=False, help="Useful only for FPTAS. A float number from interval (0; 100]. Represents highest possible mistake in percents.")
@click.option("--check-time", type=bool, default=True, help="Should the result also check elapsed time.")
@click.option("--time-retries", type=int, default=1, help="How many times should we retry if elapsed time is checked.")
@click.argument("input-file", type=click.File("r"), required=True)
@click.argument("output-dir", required=True)
def file(strategy, relative_mistake, check_time, time_retries, input_file, output_dir):
    program = "/Users/petr/Documents/Projects/Python/PythonSamples/MI-PAA/HomeWork2/src/knapsackSolver.py"
    create_path(output_dir)

    # Run command
    p = Popen(["python", program, "--dataFile", input_file.name, "-s", strategy, "-e", str(relative_mistake), "--check-time", str(check_time), "--time-retries", str(time_retries)], stdin=PIPE, stdout=PIPE, stderr=STDOUT)

    output_file_name = input_file.name.split("/")[-1].replace(".dat", f'_{strategy}.dat')
    print(f'Running output for: {output_file_name}')
    with open(f'{output_dir}/{output_file_name}', "w") as output_file:
        for line in p.stdout:
            output_file.write(line.decode("utf-8"))
            output_file.flush()

@generate_output.command()
@click.option("-s", "--strategy", type=click.Choice(inputStrategies), default=inputStrategies[0], show_default=True)
@click.option("-e", "--relative-mistake", type=float, required=False, help="Useful only for FPTAS. A float number from interval (0; 100]. Represents highest possible mistake in percents.")
@click.option("--check-time", type=bool, default=True, help="Should the result also check elapsed time.")
@click.option("--time-retries", type=int, default=5, help="How many times should we retry if elapsed time is checked.")
@click.option("--start-count", type=int, default=4)
@click.option("--end-count", type=int, default=42)
@click.argument("input-dir", required=True)
@click.argument("output-dir", required=True)
def files(strategy, relative_mistake, check_time, time_retries, start_count, end_count, input_dir, output_dir):
    program = "/Users/petr/Documents/Projects/Python/PythonSamples/MI-PAA/HomeWork2/src/knapsackSolver.py"
    create_path(output_dir)

    create_columns_description_file(strategy, check_time, output_dir)

    files_dict = get_files_dict(input_dir)

    for key, path in files_dict.items():
        files_dict[key] = [path for path in files_dict[key] if "_inst" in path][0]

    for n_key in sorted(files_dict):
        if n_key < start_count:
            continue
        elif n_key >= end_count:
            break

        # Run command
        popen_command = ["python", program, "--dataFile", files_dict[n_key], "-s", strategy, "--check-time", str(check_time), "--time-retries", str(time_retries)]

        if relative_mistake is not None:
            popen_command.extend(["-e", str(relative_mistake)])
        
        p = Popen(popen_command, stdin=PIPE, stdout=PIPE, stderr=STDOUT)

        suffix = f"_{strategy}"

        if relative_mistake is not None:
            suffix = f"{suffix}_{str(relative_mistake).replace('.', ',')}"

        output_file_name = files_dict[n_key].split("/")[-1].replace(".dat", f'{suffix}.dat')
        print(f'Running output for: {output_file_name}. Started {time.strftime("%H:%M:%S %d.%m.")}')
        with open(f'{output_dir}/{output_file_name}', "w") as output_file:
            for line in p.stdout:
                output_file.write(line.decode("utf-8"))
                output_file.flush()

if  __name__ == "__main__":
    generate_output()   # pylint: disable=no-value-for-parameter