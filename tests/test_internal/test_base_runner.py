import pytest
from flexmock import flexmock
from typing import Dict
from algorithm_tester.concurrency_runners import Runner, Runners, BaseRunner
import algorithm_tester.concurrency_runners as concurrency_runners
from algorithm_tester_common.tester_dataclasses import Algorithm, AlgTesterContext
from algorithm_tester.helpers import curr_time_millis
from tests.test_internal.fixtures import base_context, create_dummy_algorithm, get_base_parsed_data

_runner: BaseRunner = BaseRunner()

def _removing_perform(context: AlgTesterContext, parsed_data: Dict[str, object]):
    return dict()

@pytest.mark.parametrize('algorithm', 
    (create_dummy_algorithm(),
    create_dummy_algorithm(name="DummyRemovingAlgorithm", perform_func=_removing_perform))
)
def test_get_solution_for_instance(base_context, algorithm: Algorithm):
    base_data = get_base_parsed_data(base_context, algorithm)

    res: Dict[str, object] = _runner.get_solution_for_instance(base_context, algorithm, base_data)

    assert "algorithm" in res
    assert "algorithm_name" in res
    assert "output_filename" in res

    print