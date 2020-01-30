import os
import re
import pytest
from flexmock import flexmock
from typing import Dict, List, IO
from algorithm_tester.concurrency_runners import Runner, Runners, BaseRunner
import algorithm_tester.concurrency_runners as concurrency_runners
from algorithm_tester_common.tester_dataclasses import Algorithm, AlgTesterContext, Parser, InstancesLogger
from algorithm_tester.helpers import curr_time_millis, create_path
from tests.test_internal.fixtures import create_dummy_context, create_dummy_algorithm, get_base_parsed_data, create_dummy_parser
from algorithm_tester.plugins import Plugins

_runner: BaseRunner = BaseRunner()

def test_notify_communicators_timing():
    base_context = create_dummy_context()
    notification_vars = {
        "last_comm_time": 0,
        "instances_done": 0
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
    """
    A function that does not return input data that is further needed in the algorithm.
    
    Arguments:
        context {AlgTesterContext} -- Used context.
        parsed_data {Dict[str, object]} -- Input data.
    
    Returns:
        Dict[str, object] -- Modified input data.
    """
    return {"id": parsed_data["id"], "item_count": parsed_data["item_count"]}

@pytest.mark.parametrize('algorithm', 
    (create_dummy_algorithm(),
    create_dummy_algorithm(name="DummyRemovingAlgorithm", perform_func=_removing_perform))
)
def test_get_solution_for_instance(algorithm: Algorithm):
    base_context = create_dummy_context(algorithms=[algorithm.get_name()])
    base_data = get_base_parsed_data(base_context, algorithm)
    base_data.update({"id": 0, "item_count": 0})

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

@pytest.mark.parametrize('algorithms', 
    ([create_dummy_algorithm(), create_dummy_algorithm("Alg2")],
    [create_dummy_algorithm(name="DummyRemovingAlgorithm", perform_func=_removing_perform), create_dummy_algorithm("Alg2")])
)
def test_run_tester_for_file(algorithms: Algorithm, tmpdir):
    output_dir = tmpdir
    parser = create_dummy_parser()
    base_context: AlgTesterContext = create_dummy_context(algorithms=[alg.get_name() for alg in algorithms], parser=parser.get_name())
    base_context.num_of_instances = 500*len(algorithms)
    base_context.output_dir = output_dir.strpath

    notification_vars = {
        "last_comm_time": 0,
        "instances_done": 0,
        "instances_failed": 0
    }

    instances_logger: InstancesLogger = InstancesLogger(base_context.output_dir, base_context.is_forced)
    create_path(base_context.output_dir)
    
    flexmock(Plugins)
    Plugins.should_receive("get_parser").and_return(parser)
    
    for algorithm in algorithms:
        (Plugins.should_receive("get_algorithm")
            .with_args(algorithm.get_name())
            .and_return(algorithm))

    flexmock(BaseRunner)
    BaseRunner.should_receive("notify_communicators").times(base_context.num_of_instances + 1)

    flexmock(parser).should_receive("write_result_to_file").times(base_context.num_of_instances)

    _runner.init(instances_logger)
    _runner.run_tester_for_file(base_context, f'{base_context.input_dir}/4_inst.dat', notification_vars)

    assert notification_vars["instances_done"] == base_context.num_of_instances

    assert not instances_logger._instance_log.closed
    instances_logger.close_log()
    assert instances_logger._instance_log.closed

    instances_logger.load_instances()
    assert instances_logger.get_num_of_done_instances() == base_context.num_of_instances
    

    print

def _dummy_failing_func(context: AlgTesterContext, parsed_data: Dict[str, object]) -> Dict[str, object]:
    raise Exception("Dummy exception")

def test_run_tester_for_file_exceptions(tmpdir):
    output_dir = tmpdir
    parser = create_dummy_parser()
    algorithms = [create_dummy_algorithm(), create_dummy_algorithm(name="AlgFailure", perform_func=_dummy_failing_func)]
    base_context: AlgTesterContext = create_dummy_context(parser=parser.get_name(), algorithms=[alg.get_name() for alg in algorithms])
    base_context.num_of_instances = 500
    base_context.output_dir = output_dir.strpath

    notification_vars = {
        "last_comm_time": 0,
        "instances_done": 0,
        "instances_failed": 0
    }

    instances_logger: InstancesLogger = InstancesLogger(base_context.output_dir, base_context.is_forced)
    create_path(base_context.output_dir)
    
    flexmock(Plugins)
    Plugins.should_receive("get_parser").and_return(parser)
    
    for algorithm in algorithms:
        (Plugins.should_receive("get_algorithm")
            .with_args(algorithm.get_name())
            .and_return(algorithm))

    flexmock(BaseRunner)
    BaseRunner.should_receive("notify_communicators").times(base_context.num_of_instances + 1)

    flexmock(parser).should_receive("write_result_to_file").times(base_context.num_of_instances)

    _runner.init(instances_logger)
    _runner.run_tester_for_file(base_context, f'{base_context.input_dir}/4_inst.dat', notification_vars)

    assert notification_vars["instances_done"] == base_context.num_of_instances
    assert notification_vars["instances_failed"] == base_context.num_of_instances
    print

@pytest.mark.parametrize('is_change_forced', (True, False))
def test_compute_results(is_change_forced: bool):
    base_context: AlgTesterContext = create_dummy_context()
    base_context.max_files_to_check = None
    base_context.is_forced = is_change_forced
    instances_logger: InstancesLogger = InstancesLogger(base_context.output_dir, base_context.is_forced)

    input_files = list()
    for root, _, files in os.walk(base_context.input_dir):
        for filename in files:
            input_files.append(f'{root}/{filename}')

    flexmock(BaseRunner)
    (BaseRunner.should_receive("run_tester_for_file")
        .with_args(base_context, re.compile(f'{base_context.input_dir}/.*'), object)
        .and_return(None)
        .times(len(input_files)))

    _runner.init(instances_logger)
    _runner.compute_results(base_context, input_files)

    print