import pytest
from flexmock import flexmock
from typing import List, Dict
from algorithm_tester_common.tester_dataclasses import AlgTesterContext, Algorithm

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
        min_time_between_communications = 10.0,
        start_time = 0,
        num_of_instances = 100
    )

    return dummy_context

def get_base_parsed_data(base_context: AlgTesterContext, algorithm: Algorithm) -> Dict[str, object]:
    dummy_data = dict()
    dummy_data["output_filename"] = "output_filename"
    dummy_data["algorithm_name"] = algorithm.get_name()
    dummy_data["algorithm"] = algorithm

    return dummy_data

def _base_perform(context: AlgTesterContext, parsed_data: Dict[str, object]) -> Dict[str, object]:
    return parsed_data

def create_dummy_algorithm(columns: List[str] = ["A", "B", "C"], name: str = "DummyAlgorithm", perform_func = _base_perform):
    class DummyAlgorithm(Algorithm):

        def get_name(self) -> str:
            return name 

        def get_columns(self, show_time: bool = True) -> List[str]:
            return columns

        def perform_algorithm(self, context: AlgTesterContext, parsed_data: Dict[str, object]) -> Dict[str, object]:
            return perform_func(context, parsed_data)

    return DummyAlgorithm()