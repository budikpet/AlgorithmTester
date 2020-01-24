import os
import timeit
import time
from typing import Dict, List, IO
from algorithm_tester.helpers import get_input_files, create_path
from algorithm_tester_common.tester_dataclasses import AlgTesterContext, Algorithm, Parser
from algorithm_tester.plugins import plugins
from algorithm_tester.concurrency_runners import Runner, Runners

"""
Contains main logic of the application.
"""

def count_instances(context: AlgTesterContext, parser_name: str, input_files: List[str]):

    parser: Parser = plugins.get_parser(parser_name)
    context.num_of_instances = 0
    for input_file in input_files:
        with open(input_file) as instance_file:
            context.num_of_instances += parser.get_num_of_instances(context, instance_file)
            instance_file.seek(0)

def run_tester(algorithms: List[str], concurrency_runner: str, check_time: bool, time_retries: int, parser: str, communicators: List[str], max_num: int, input_dir, output_dir, extra_options):
    """
    Get all data provided by click CLI interface. Run the whole programme.
    
    Arguments:
        algorithms {List[str]} -- List of names of all algorithms that are to be used.
        concurrency_runner {str} -- Name of the concurrency runner that is to be used.
        check_time {bool} -- True if we want to check actual time of the execution.
        time_retries {int} -- If check_time is True, then this number indicates how many times should the computation be repeated to get more accurate results.
        parser {str} -- Name of the parser that is to be used.
        communicators {List[str]} -- [description]
        max_num {int} -- How many files should be checked at most.
        input_dir {[type]} -- [description]
        output_dir {[type]} -- [description]
        extra_options {[type]} -- [description]
    """

    runner: Runner = Runners[concurrency_runner].value
    input_files: List[str] = get_input_files(input_dir)
    context: AlgTesterContext = AlgTesterContext(
        algorithms=algorithms, parser=parser, communicators=communicators, concurrency_runner=concurrency_runner,
        max_num=max_num, check_time=check_time, time_retries=time_retries,
        extra_options=extra_options,
        input_dir=input_dir, output_dir=output_dir
        )

    create_path(output_dir)

    # Count number of instances
    count_instances(context, parser, input_files)

    context.start_time = time.perf_counter()
    runner.compute_results(context, input_files)
    finish = time.perf_counter()
    print(f'Finished task in {round(finish - context.start_time, 2)} second(s)')

    print(f'Algorithm ended at {time.strftime("%H:%M:%S %d.%m.")}')