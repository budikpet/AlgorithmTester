import os
import re
import pytest
from flexmock import flexmock
from typing import Dict, List, IO
from algorithm_tester.concurrency_runners import Runner, Runners, BaseRunner
import algorithm_tester.concurrency_runners as concurrency_runners
from algorithm_tester_common.tester_dataclasses import Algorithm, AlgTesterContext, Parser
from algorithm_tester.helpers import curr_time_millis
from tests.test_internal.fixtures import create_dummy_context, create_dummy_algorithm, get_base_parsed_data, create_dummy_parser
from algorithm_tester.plugins import Plugins

_runner: BaseRunner = BaseRunner()

def test_notify_communicators_timing():
    base_context = create_dummy_context()
    notification_vars = {
        "last_comm_time": 0,
        "instances_done_cnt": 0
    }

    res = _runner.notify_communicators(base_context, [], {}, notification_vars)
    new_last_comm_time = notification_vars["last_comm_time"]
    assert notification_vars["last_comm_time"] != 0
    assert res == True

    res = _runner.notify_communicators(base_context, [], {}, notification_vars)
    assert res == False
    assert notification_vars["last_comm_time"] == new_last_comm_time

    notification_vars["last_comm_time"] -= base_context.min_time_between_communications + 1
    new_last_comm_time = notification_vars["last_comm_time"]
    res = _runner.notify_communicators(base_context, [], {}, notification_vars)
    assert res == True
    assert notification_vars["last_comm_time"] != new_last_comm_time

    print

def _removing_perform(context: AlgTesterContext, parsed_data: Dict[str, object]):
    return dict()

@pytest.mark.parametrize('algorithm', 
    (create_dummy_algorithm(),
    create_dummy_algorithm(name="DummyRemovingAlgorithm", perform_func=_removing_perform))
)
def test_get_solution_for_instance(algorithm: Algorithm):
    base_context = create_dummy_context(algorithms=[algorithm.get_name()])
    base_data = get_base_parsed_data(base_context, algorithm)

    res: Dict[str, object] = _runner.get_solution_for_instance(base_context, algorithm, base_data)

    assert "algorithm" in res
    assert "algorithm_name" in res
    assert "output_filename" in res

    print

@pytest.mark.parametrize('algorithm', 
    (create_dummy_algorithm(),
    create_dummy_algorithm(name="DummyRemovingAlgorithm", perform_func=_removing_perform))
)
def test_get_parsed_instances_data(algorithm: Algorithm):
    parser = create_dummy_parser()
    base_context = create_dummy_context(algorithms=[algorithm.get_name()], parser=parser.get_name())
    base_data = get_base_parsed_data(base_context, algorithm)

    with open(f'{base_context.input_dir}/4_inst.dat', "r") as input_file:
        res: List[Dict[str, object]] = _runner.get_parsed_instances_data(base_context, input_file, parser, algorithm)

    assert len(res) > 0
    assert "algorithm" in res[0]
    assert "algorithm_name" in res[0]
    assert "output_filename" in res[0]

    print

@pytest.mark.parametrize('algorithm', 
    (create_dummy_algorithm(),
    create_dummy_algorithm(name="DummyRemovingAlgorithm", perform_func=_removing_perform))
)
def test_run_tester_for_file(algorithm: Algorithm, tmpdir):
    output_dir = tmpdir
    parser = create_dummy_parser()
    base_context: AlgTesterContext = create_dummy_context(algorithms=[algorithm.get_name()], parser=parser.get_name())
    base_context.num_of_instances = 500
    base_context.output_dir = output_dir.strpath

    notification_vars = {
        "last_comm_time": 0,
        "instances_done_cnt": 0
    }
    
    flexmock(Plugins)
    Plugins.should_receive("get_parser").and_return(parser)
    Plugins.should_receive("get_algorithm").and_return(algorithm)

    flexmock(BaseRunner)
    BaseRunner.should_receive("notify_communicators").times(base_context.num_of_instances + 1)

    flexmock(parser).should_receive("write_result_to_file").times(base_context.num_of_instances)

    _runner.run_tester_for_file(base_context, f'{base_context.input_dir}/4_inst.dat', notification_vars)

    assert notification_vars["instances_done_cnt"] == base_context.num_of_instances
    print

def test_compute_results():
    base_context: AlgTesterContext = create_dummy_context()
    base_context.max_num = None

    input_files = list()
    for root, _, files in os.walk(base_context.input_dir):
        for filename in files:
            input_files.append(f'{root}/{filename}')

    flexmock(BaseRunner)
    (BaseRunner.should_receive("run_tester_for_file")
        .with_args(base_context, re.compile(f'{base_context.input_dir}/.*'), object)
        .and_return(None)
        .times(len(input_files)))

    _runner.compute_results(base_context, input_files)

    print