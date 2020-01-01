from flexmock import flexmock
import pytest
from algorithm_tester.concurrency_runners import Runner, Runners, BaseRunner, ConcurrentFilesRunner, ConcurrentInstancesRunner, create_columns_description_file
from algorithm_tester_common.tester_dataclasses import Algorithm, AlgTesterContext

@pytest.fixture
def base_context() -> flexmock:
    dummy_context = flexmock(
        algorithm_names = [],
        parser_name = "DummyParser",
        communicator_names = "DummyCommunicator",
        concurrency_runner_name = "BASE",
        check_time = False,
        time_retries = 1,
        extra_options = {},
        input_dir = "",
        output_dir = "",
        batch_size = 10,
    )

    return dummy_context

def test_create_columns_description_file(base_context, tmpdir):
    output_dir = tmpdir
    base_context.output_dir = output_dir.strpath

    algorithm = flexmock(
        get_columns=lambda: ["A", "B", "C"],
        get_name=lambda: "DummyAlgorithm"
    )


    
    create_columns_description_file(base_context, algorithm)

    contents = output_dir.listdir()
    assert len(contents) == 1
    assert algorithm.get_name() in contents[0].basename

    print