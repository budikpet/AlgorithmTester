import pytest
from flexmock import flexmock
from typing import List, Dict
from algorithm_tester_common.tester_dataclasses import AlgTesterContext

@pytest.fixture
def base_context() -> flexmock:
    dummy_context = flexmock(
        algorithm_names = [],
        parser_name = "DummyParser",
        communicator_names = "",
        concurrency_runner_name = "BASE",
        check_time = False,
        time_retries = 1,
        extra_options = {},
        input_dir = "",
        output_dir = "",
        min_time_between_communications = 10000,
        start_time = 0,
        num_of_instances = 100
    )

    return dummy_context

def _base_perform(context: AlgTesterContext, parsed_data: Dict[str, object]) -> Dict[str, object]:
    return parsed_data

def create_dummy_algorithm(columns: List[str] = ["A", "B", "C"], name: str = "DummyAlgorithm", perform_func = _base_perform):
    algorithm = flexmock(
        get_columns=lambda: columns,
        get_name=lambda: name,
        perform_algorithm=lambda context, parsed_data: perform_func(context, parsed_data)
    )

    return algorithm