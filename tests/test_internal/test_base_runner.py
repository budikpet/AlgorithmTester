import pytest
from flexmock import flexmock
from typing import Dict, List, IO
from algorithm_tester.concurrency_runners import Runner, Runners, BaseRunner
import algorithm_tester.concurrency_runners as concurrency_runners
from algorithm_tester_common.tester_dataclasses import Algorithm, AlgTesterContext
from algorithm_tester.helpers import curr_time_millis
from tests.test_internal.fixtures import create_dummy_context, create_dummy_algorithm, get_base_parsed_data, create_dummy_parser

_runner: BaseRunner = BaseRunner()

def _removing_perform(context: AlgTesterContext, parsed_data: Dict[str, object]):
    return dict()

@pytest.mark.parametrize('algorithm', 
    (create_dummy_algorithm(),
    create_dummy_algorithm(name="DummyRemovingAlgorithm", perform_func=_removing_perform))
)
def test_get_solution_for_instance(algorithm: Algorithm):
    base_context = create_dummy_context()
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
    base_context = create_dummy_context()
    base_data = get_base_parsed_data(base_context, algorithm)
    parser = create_dummy_parser()

    with open(f'{base_context.input_dir}/4_inst.dat', "r") as input_file:
        res: List[Dict[str, object]] = _runner.get_parsed_instances_data(base_context, input_file, parser, algorithm)

    assert len(res) > 0
    assert "algorithm" in res[0]
    assert "algorithm_name" in res[0]
    assert "output_filename" in res[0]

    print