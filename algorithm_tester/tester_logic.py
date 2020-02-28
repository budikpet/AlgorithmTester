import os
import timeit
import time
import shutil
from typing import Dict, List, IO
from algorithm_tester_common.tester_dataclasses import AlgTesterContext, Algorithm, Parser
from algorithm_tester.plugins import plugins
from algorithm_tester.concurrency_runners import Runner, Runners
import algorithm_tester.helpers as helpers

"""
Contains main logic of the application.
"""

def count_instances(context: AlgTesterContext, input_files: List[str]):
    """
    Count instances of all instance files and stores the value in context.
    
    Arguments:
        context {AlgTesterContext} -- Used context.
        input_files {List[str]} -- List of all input files.
    """

    parser: Parser = plugins.get_parser(context.parser_name)
    context.num_of_instances = 0
    for input_file in input_files:
        with open(f'{context.input_dir}/{input_file}') as instance_file:
            context.num_of_instances += parser.get_num_of_instances(context, instance_file)
            instance_file.seek(0)
    
    context.num_of_instances *= len(context.algorithm_names)

def run_tester(algorithms: List[str], concurrency_runner: str, check_time: bool, time_retries: int, parser: str, communicators: List[str], max_num: int, is_forced: True, min_communicator_delay: float, input_dir, output_dir, extra_options):
    """
    Get all data provided by click CLI interface. Run the whole programme.
    
    Arguments:
        algorithms {List[str]} -- List of names of all algorithms that are to be used.
        concurrency_runner {str} -- Name of the concurrency runner that is to be used.
        check_time {bool} -- True if we want to check actual time of the execution.
        time_retries {int} -- If check_time is True, then this number indicates how many times should the computation be repeated to get more accurate results.
        parser {str} -- Name of the parser that is to be used.
        communicators {List[str]} -- List of all used communicators.
        max_num {int} -- How many files should be checked at most.
        min_communicator_delay {float} -- How many seconds between two communicator messages.
        input_dir {[type]} -- Directory of all files with instances.
        output_dir {[type]} -- Directory where the programme will store output files.
        extra_options {[type]} -- Other options that algorithms need.
    """

    runner: Runner = Runners[concurrency_runner].value
    input_files: List[str] = helpers.get_input_files(input_dir)
    context: AlgTesterContext = AlgTesterContext(
        algorithms=algorithms, parser=parser, communicators=communicators, concurrency_runner=concurrency_runner,
        max_num=max_num, check_time=check_time, time_retries=time_retries, min_communicator_delay=min_communicator_delay,
        extra_options=extra_options, is_forced = is_forced,
        input_dir=input_dir, output_dir=output_dir
        )

    helpers.create_path(output_dir)

    # Count number of instances
    count_instances(context, input_files)

    # Remove instance files if forced = True
    if context.is_forced:
        shutil.rmtree(context.output_dir)
        helpers.create_path(output_dir)


    context.start_time = helpers.curr_time_millis()
    start = time.perf_counter()
    runner.compute_results(context, input_files)
    finish = time.perf_counter()
    print(f'Finished task in {round(finish - start, 2)} second(s)')

    print(f'Algorithm ended at {time.strftime("%H:%M:%S %d.%m.")}')