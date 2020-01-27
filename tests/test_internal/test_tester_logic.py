import os
import pytest
import flexmock
import algorithm_tester.tester_logic as tester_logic
from algorithm_tester.concurrency_runners import Runner, BaseRunner, ConcurrentFilesRunner, ConcurrentInstancesRunner
from algorithm_tester.plugins import Plugins
from algorithm_tester_common.tester_dataclasses import AlgTesterContext, Algorithm, Parser, Communicator
from tests.test_internal.fixtures import create_dummy_context, create_dummy_algorithm, get_base_parsed_data, create_dummy_parser 

def test_count_instances():
    parser: Parser = create_dummy_parser()
    ctx: AlgTesterContext = create_dummy_context(parser=parser)

    input_files = list()
    for _, _, files in os.walk(ctx.input_dir):
        for filename in files:
            input_files.append(filename)

    flexmock(Plugins)
    (Plugins.should_receive("get_parser").and_return(parser))

    tester_logic.count_instances(ctx, input_files)

    assert ctx.num_of_instances == 500*2
    print

def test_run_tester(tmpdir):
    parser: Parser = create_dummy_parser()
    algorithms = ["Alg1", "Alg2"]
    communicators = ["Slack"]
    ctx: AlgTesterContext = create_dummy_context(parser=parser, algorithms=algorithms, communicators=communicators)
    ctx.output_dir = f'{tmpdir.strpath}/Test'

    input_files = list()
    for _, _, files in os.walk(ctx.input_dir):
        for filename in files:
            input_files.append(filename)

    flexmock(Plugins)
    (Plugins.should_receive("get_parser").and_return(parser))

    flexmock(BaseRunner)
    (BaseRunner.should_receive("compute_results")
        .with_args(object, input_files)
        .and_return(None)
        .once())

    assert not os.path.isdir(ctx.output_dir)
    
    tester_logic.run_tester(ctx.algorithm_names, ctx.concurrency_runner_name, ctx.check_time, ctx.time_retries, ctx.parser_name, ctx.communicator_names, ctx.max_num, ctx.min_time_between_communications, ctx.input_dir, ctx.output_dir, ctx.extra_options)

    assert os.path.isdir(ctx.output_dir)

    print