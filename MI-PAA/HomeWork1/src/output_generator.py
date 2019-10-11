from subprocess import Popen, PIPE, STDOUT
import click
from typing import Dict
import os
from solverStrategy import Strategies
from myDataClasses import Modes
from helpers import get_files_dict, create_clean_folder

inputStrategies = [strategy.name for strategy in Strategies]
inputModes = [mode.name for mode in Modes]

@click.command()
@click.option("-s", "--strategy", type=click.Choice(inputStrategies), default=inputStrategies[0], show_default=True)
@click.option("--start-count", type=int, default=4)
@click.option("--end-count", type=int, default=42)
@click.argument("input-dir", required=True)
@click.argument("output-dir", required=True)
def generate_output(strategy, start_count, end_count, input_dir, output_dir):
    program = "/home/petr/Documents/LocalShared/PythonSamples/MI-PAA/HomeWork1/src/knapsackSolver.py"

    create_clean_folder(output_dir)

    files_dict = get_files_dict(input_dir)

    for key, path in files_dict.items():
        files_dict[key] = [path for path in files_dict[key] if "_inst" in path][0]

    for n_key in sorted(files_dict):
        if n_key < start_count:
            continue
        elif n_key >= end_count:
            break

        # Run command
        p = Popen(["python", program, "--dataFile", files_dict[n_key], "-s", strategy], stdin=PIPE, stdout=PIPE, stderr=STDOUT)

        output_file_name = files_dict[n_key].split("/")[-1].replace(".dat", f'_{strategy}.dat')
        print(f'Running output for: {output_file_name}')
        with open(f'{output_dir}/{output_file_name}', "w") as output_file:
            for line in p.stdout:
                output_file.write(line.decode("utf-8"))
                output_file.flush()
        print

if  __name__ == "__main__":
    generate_output()   # pylint: disable=no-value-for-parameter