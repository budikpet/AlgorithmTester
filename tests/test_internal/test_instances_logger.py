import os
import pytest
from flexmock import flexmock
from algorithm_tester.concurrency_runners import get_click_options
from algorithm_tester_common.tester_dataclasses import InstancesLogger, Parser, AlgTesterContext, Algorithm
from tests.test_internal.fixtures import create_dummy_algorithm, create_dummy_context, create_dummy_parser

log_filename = ".instances_log.dat"

def create_dummy_results(context: AlgTesterContext, algorithm: Algorithm, parser: Parser, log_filename: str, max_instances_done_per_file: int = None):
    """
    Generates test results and log.
    
    Arguments:
        context {AlgTesterContext} -- [description]
        algorithm {Algorithm} -- [description]
        parser {Parser} -- [description]
        log_filename {str} -- [description]
    
    Keyword Arguments:
        max_instances_done_per_file {int} -- [description] (default: {None})
    """
    with open(f'{context.output_dir}/{log_filename}', "w") as log_file:
        for root, _, files in os.walk(context.input_dir):
            for filename in files:
                with open(f'{root}/{filename}', "r") as input_file:
                    real_num_of_instances: int = parser.get_num_of_instances(context, input_file)
                    input_file.seek(0)
                    if max_instances_done_per_file is None:
                        max_instances_done_per_file = real_num_of_instances

                    click_options = get_click_options(context, algorithm)
                    output_filename: str = parser.get_output_file_name(context, input_file, click_options)
                    with open(f'{context.output_dir}/{output_filename}', "w") as output_file:
                        for _ in range(min(real_num_of_instances, max_instances_done_per_file)):
                            # Create results
                            instance_data = parser.get_next_instance(input_file)
                            instance_data["output_filename"] = output_filename
                            instance_data["algorithm_name"] = algorithm.get_name()
                            instance_data["algorithm"] = algorithm
                            instance_identifier: str = parser._get_complete_instance_identifier(algorithm, instance_data)
                            log_file.write(f'{instance_identifier}\n')
                            parser.write_result_to_file(output_file, instance_data)

    print

@pytest.mark.parametrize('max_instances_done_per_file', (None, 10))
def test_create_dummy_results(tmpdir, max_instances_done_per_file: int):
    parser: Parser = create_dummy_parser(write_result=True)
    algorithm: Algorithm = create_dummy_algorithm()
    base_context: AlgTesterContext = create_dummy_context(parser=parser.get_name(), algorithms=[algorithm.get_name()])
    base_context.max_files_to_check = None
    base_context.output_dir = tmpdir.strpath
    num_of_input_files = len(os.listdir(base_context.input_dir))

    assert len(os.listdir(base_context.output_dir) ) == 0

    create_dummy_results(base_context, algorithm, parser, log_filename, max_instances_done_per_file)

    assert len(os.listdir(base_context.output_dir) ) == num_of_input_files + 1
    assert log_filename in os.listdir(base_context.output_dir)
    
    with open(f'{base_context.output_dir}/{log_filename}', "r") as log_file:
        for num_of_logs, _ in enumerate(log_file):
            pass
        num_of_logs += 1

    assert num_of_logs != 0

    if max_instances_done_per_file is not None:
        assert num_of_logs == num_of_input_files * max_instances_done_per_file

def prepare_objects(output_dir, is_change_forced: bool, max_instances_done_per_file: int):
    parser: Parser = create_dummy_parser(write_result=True)
    algorithm: Algorithm = create_dummy_algorithm()
    base_context: AlgTesterContext = create_dummy_context(parser=parser.get_name(), algorithms=[algorithm.get_name()])
    base_context.max_files_to_check = None
    base_context.is_forced = is_change_forced
    base_context.output_dir = output_dir

    create_dummy_results(base_context, algorithm, parser, log_filename, max_instances_done_per_file)

    instances_logger = InstancesLogger(base_context.output_dir, base_context.is_forced)

    return base_context, algorithm, parser, instances_logger


@pytest.mark.parametrize(['is_change_forced', 'max_instances_done_per_file'], 
    [
        (True, None),
        (True, 10),
        (False, None),
        (False, 10)
    ]
)
def test_init(tmpdir, is_change_forced: bool, max_instances_done_per_file: int):
    base_context, algorithm, parser, instances_logger = prepare_objects(tmpdir.strpath, is_change_forced, max_instances_done_per_file)

    num_of_input_files = len(os.listdir(base_context.input_dir))
    
    if not is_change_forced:
        assert algorithm.get_name() in instances_logger._loaded_instances
        assert len(instances_logger._loaded_instances[algorithm.get_name()]) != 0
        if max_instances_done_per_file is not None:
            assert len(instances_logger._loaded_instances[algorithm.get_name()]) == max_instances_done_per_file*num_of_input_files
    else:
        assert algorithm.get_name() not in instances_logger._loaded_instances
        assert not os.path.isdir(base_context.output_dir)

    print

def test_init_no_log(tmpdir):
    base_context, algorithm, parser, _ = prepare_objects(tmpdir.strpath, False, None)
    os.remove(f'{base_context.output_dir}/{log_filename}')

    instances_logger: InstancesLogger = InstancesLogger(base_context.output_dir, base_context.is_forced)

    num_of_input_files = len(os.listdir(base_context.input_dir))
    
    assert algorithm.get_name() not in instances_logger._loaded_instances
    assert os.path.isdir(base_context.output_dir)
    assert len(os.listdir(base_context.output_dir) ) == num_of_input_files

    print

@pytest.mark.parametrize(['is_change_forced', 'max_instances_done_per_file'], 
    [
        (True, None),
        (True, 10),
        (False, None),
        (False, 10)
    ]
)
def test_get_num_of_done_instances(tmpdir, is_change_forced: bool, max_instances_done_per_file: int):
    base_context, algorithm, parser, instances_logger = prepare_objects(tmpdir.strpath, is_change_forced, max_instances_done_per_file)
   
    num_of_input_files = len(os.listdir(base_context.input_dir))

    if is_change_forced:
        assert instances_logger.get_num_of_done_instances() == 0
    else:
        if max_instances_done_per_file is None:
            assert instances_logger.get_num_of_done_instances() != 0
        else:
            assert instances_logger.get_num_of_done_instances() == num_of_input_files*max_instances_done_per_file