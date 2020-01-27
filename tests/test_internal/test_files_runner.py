import os
import re
import pytest
from flexmock import flexmock
from typing import Dict, List, IO
from algorithm_tester.concurrency_runners import Runner, Runners, BaseRunner, ConcurrentFilesRunner
import algorithm_tester.concurrency_runners as concurrency_runners
from algorithm_tester_common.tester_dataclasses import Algorithm, AlgTesterContext, Parser
from algorithm_tester.helpers import curr_time_millis
from tests.test_internal.fixtures import create_dummy_context, create_dummy_algorithm, get_base_parsed_data, create_dummy_parser
from algorithm_tester.plugins import Plugins
from io import TextIOWrapper

_runner: ConcurrentFilesRunner = ConcurrentFilesRunner()

def _get_input_files(path: str, mode: str = "r"):
    files_dict: Dict[str, IO] = dict()

    for root, _, files in os.walk(path):
        for filename in files:
            files_dict[filename] = open(f'{root}/{filename}', mode)

    return files_dict

def test_close_all_files(tmpdir):
    file_cnt = 10
    closed_files_cnt = 3

    currently_closed_files = 0
    files_dict: Dict[str, IO] = dict()
    for i in range(file_cnt):
        filename = f'file_{i}'
        files_dict[filename] = open(f'{tmpdir.strpath}/{filename}', 'w')

        if currently_closed_files < closed_files_cnt:
            files_dict[filename].close()
            currently_closed_files += 1

    _runner.close_all_files(files_dict)

    for file in files_dict.values():
        assert file.closed

    print

def test_get_base_instances():
    parser = create_dummy_parser()
    base_context: AlgTesterContext = create_dummy_context(parser=parser)
    base_context.num_of_instances = 500*2
    input_files = _get_input_files(base_context.input_dir)

    instance_cnt = 0
    for (instance, file) in _runner.get_base_instances(input_files, parser):
        assert instance is not None
        assert file is not None
        assert file.closed == False
        instance_cnt += 1

    assert instance_cnt == base_context.num_of_instances
    
    _runner.close_all_files(input_files)

def test_get_data_for_executor():
    parser = create_dummy_parser()
    algorithms = [create_dummy_algorithm(name="DummyAlg1"), create_dummy_algorithm(name="DummyAlg2")]
    base_context: AlgTesterContext = create_dummy_context(parser=parser)
    base_context.num_of_instances = 500*2*len(algorithms)
    input_files = _get_input_files(base_context.input_dir)

    instance_cnt = 0
    for (algorithm, data) in _runner.get_data_for_executor(base_context, input_files, parser, algorithms):
        assert algorithm in algorithms
        instance_cnt += 1

    assert instance_cnt == base_context.num_of_instances
    
    _runner.close_all_files(input_files)

def test_write_result(tmpdir):
    parser = create_dummy_parser()
    base_context: AlgTesterContext = create_dummy_context(parser=parser)
    base_context.output_dir = tmpdir.strpath
    output_files = {
        'output_1.dat': open(f'{base_context.output_dir}/output_1.dat', "w")
    }

    flexmock(parser).should_receive("write_result_to_file").times(3)

    _runner.write_result(base_context, parser, output_files, {"output_filename": "output_1.dat"})
    assert len(output_files.keys()) == 1

    _runner.write_result(base_context, parser, output_files, {"output_filename": "output_2.dat"})
    assert len(output_files.keys()) == 2

    _runner.write_result(base_context, parser, output_files, {"output_filename": "output_1.dat"})
    assert len(output_files.keys()) == 2

    _runner.close_all_files(output_files)
    print

# def tests_run_tester_for_data(tmpdir):
#     parser = create_dummy_parser()
#     algorithms = [create_dummy_algorithm(name="DummyAlg1"), create_dummy_algorithm(name="DummyAlg2")]
#     base_context: AlgTesterContext = create_dummy_context(parser=parser)
#     base_context.num_of_instances = 500*2*len(algorithms)
#     base_context.output_dir = tmpdir.strpath
#     input_files_dict = _get_input_files(base_context.input_dir)
#     output_files_dict = dict()

#     (flexmock(_runner._base_runner).should_receive("notify_communicators")
#         .and_return(None)
#         .times(base_context.num_of_instances + 1))

#     (flexmock(_runner).should_receive("write_result")
#         .and_return(None)
#         .times(base_context.num_of_instances)
#         )

#     _runner.run_tester_for_data(base_context, algorithms, parser, list(), input_files_dict, output_files_dict)
#     print