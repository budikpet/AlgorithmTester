import click
import time
from typing import List
from algorithm_tester.plugins import plugins
from algorithm_tester.tester_logic import run_tester
from algorithm_tester.decorators import docstring_parameters, use_dynamic_options
from algorithm_tester.validators import validate_algorithms, validate_parser, validate_extra_options, validate_concurrency_runner, validate_communicators
from algorithm_tester.concurrency_runners import Runners, Runner

"""
Click CLI interface for the application.
"""


@click.command(name='my-cmd', context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.option("-s", "--algorithms", callback=validate_algorithms, required=True, default=",".join(plugins.get_algorithm_names()), show_default=True, help="CSV string of names of available algorithms.")
@click.option("-r", "--concurrency-runner", callback=validate_concurrency_runner, required=True, default=f'{Runners.BASE.name}', show_default=True, help="Concurrency mode the programme should use to compute results.")
@click.option("--check-time", type=bool, default=False, help="Should the result also check elapsed time.")
@click.option("--time-retries", type=int, default=1, help="How many times should we retry if elapsed time is checked.")
@click.option("-p", "--parser", type=str, callback=validate_parser, required=True, help="Name of the parser that is used to parse input files.")
@click.option("-c", "--communicators", type=str, callback=validate_communicators, required=False, default=",".join(plugins.get_communicator_names()), show_default=True, help="CSV string of names of available communication interfaces.")
@click.option("-n", "--max-num", type=int, required=False, help="If set then the run_tester uses only (0, max-num] of input files.")
@click.option("--input-dir", type=str, required=True, help="Path to directory with input files.")
@click.option("--output-dir", type=str, required=True, help="Path to directory where output files are to be stored.")
@click.argument('extra-options', callback=validate_extra_options, nargs=-1, type=click.UNPROCESSED)
def run_tester_cli_interface(algorithms: List[str], concurrency_runner: str, check_time: bool, time_retries: int, parser: str, communicators: List[str], max_num: int, input_dir, output_dir, extra_options):
    run_tester(algorithms, concurrency_runner, check_time, time_retries, parser, communicators, max_num, input_dir, output_dir, extra_options)

def main(prog_name: str):
    run_tester_cli_interface(prog_name=prog_name)   # pylint: disable=no-value-for-parameter,unexpected-keyword-arg