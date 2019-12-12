import click
from typing import List
from algorithm_tester.plugins import plugins
from algorithm_tester.helpers import get_files_dict, create_path
from algorithm_tester.tester_dataclasses import TesterContext
from algorithm_tester.tester_logic import run_algorithms_for_file
from algorithm_tester.decorators import docstring_parameters, use_dynamic_options
from algorithm_tester.validators import validate_algorithms, validate_parser

# TODO: Parser pro parsování vstupních i výstupních souborů
# TODO: Parser bude mít metodu přijímající output-dict, podle kterého je vráceno jméno výstupního souboru.
# TODO: Parser určuje, jaké hodnoty (sloupce) jsou do výstupního souboru ukládány. Algoritmus může dodat hodnoty, které chce, aby byli přidány.

@click.command()
@click.option("-s", "--algorithms", callback=validate_algorithms, required=True, default=",".join(plugins.get_algorithm_names()), show_default=True, help="CSV string of names of available algorithms.")
@click.option("--check-time", type=bool, default=False, help="Should the result also check elapsed time.")
@click.option("--time-retries", type=int, default=1, help="How many times should we retry if elapsed time is checked.")
@click.option("-p", "--parser", type=str, callback=validate_parser, required=True, help="Name of the parser that is used to parse input files.")
@click.option("-c", "--communicators", type=str, required=False, help="CSV string of names of available communication interfaces.")
@click.option("-n", "--max-num", type=int, required=False, help="If set then the run_tester uses only (0, max-num] of input files.")
@click.argument("input-dir", required=True)
@click.argument("output-dir", required=True)
@docstring_parameters("Parametric docstring", "very nice!")
def run_tester(algorithms: List[str], check_time: bool, time_retries: int, parser: str, communicators: List[str], max_num: int, input_dir, output_dir, **kwargs):
    """

    {} is {}.
    """
    
    files_dict = get_files_dict(input_dir)

    context: TesterContext = TesterContext(
        algorithms=algorithms, parser=parser, communicators=communicators,
        max_num=max_num, check_time=check_time, time_retries=time_retries,
        other_options=kwargs,
        input_dir=input_dir, output_dir=output_dir
        )

    for key, path in files_dict.items():
        files_dict[key] = [path for path in files_dict[key] if "_inst" in path][0]

    create_path(output_dir)

    for index, n_key in enumerate(sorted(files_dict)):
        if max_num is not None:
            if index >= max_num:
                break

        with open(files_dict[n_key], "r") as input_file:
            run_algorithms_for_file(context, input_file)

def main(prog_name: str):
    run_tester(prog_name=prog_name)   # pylint: disable=no-value-for-parameter,unexpected-keyword-arg