import pytest
from flexmock import flexmock
from algorithm_tester.concurrency_runners import Runner, Runners, BaseRunner, ConcurrentFilesRunner, ConcurrentInstancesRunner, create_columns_description_file, notify_communicators
from algorithm_tester_common.tester_dataclasses import Algorithm, AlgTesterContext
from algorithm_tester.helpers import curr_time_millis
from tests.test_internal.fixtures import base_context, create_dummy_algorithm

def test_create_columns_description_file(base_context, tmpdir):
    output_dir = tmpdir
    base_context.output_dir = output_dir.strpath

    algorithm = create_dummy_algorithm()
    
    create_columns_description_file(base_context, algorithm)

    contents = output_dir.listdir()
    assert len(contents) == 1
    assert algorithm.get_name() in contents[0].basename

    with open(contents[0].strpath) as columns_file:
        line: str = columns_file.read().strip()

    assert line is not None
    assert ' '.join(algorithm.get_columns()) == line

    print