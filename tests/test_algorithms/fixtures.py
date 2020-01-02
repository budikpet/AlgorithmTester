import pytest
import flexmock

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