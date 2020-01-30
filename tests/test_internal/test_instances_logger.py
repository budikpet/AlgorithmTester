import pytest
import flexmock
from algorithm_tester_common.tester_dataclasses import InstancesLogger, Parser, AlgTesterContext, Algorithm
from tests.test_internal.fixtures import create_dummy_algorithm, create_dummy_context, create_dummy_parser

def create_dummy_results(context: AlgTesterContext):
    print

@pytest.mark.parametrize('is_change_forced', (True, False))
def test_init(tmpdir, is_change_forced: bool):
    parser: Parser = create_dummy_parser(write_result=True)
    algorithm: Algorithm = create_dummy_algorithm()
    base_context: AlgTesterContext = create_dummy_context(parser=parser.get_name(), algorithms=[algorithm.get_name()])
    base_context.max_files_to_check = None
    base_context.is_forced = is_change_forced

    

    print