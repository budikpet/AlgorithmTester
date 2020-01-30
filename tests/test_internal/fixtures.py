import pytest
from flexmock import flexmock
from typing import List, Dict, IO
from algorithm_tester_common.tester_dataclasses import AlgTesterContext, Algorithm, Parser

def create_dummy_context(algorithms: List[str] = list(), parser: Parser = "DummyParser", communicators: List[str] = list()) -> AlgTesterContext:
    context: AlgTesterContext = AlgTesterContext(
        algorithms=algorithms, 
        parser=parser, 
        communicators=communicators, 
        concurrency_runner="BASE",
        max_num=None, 
        is_forced=True,
        check_time=False, 
        time_retries=1, 
        min_communicator_delay=10.0,
        extra_options=dict(),
        input_dir="tests/test_internal/fixtures/data", 
        output_dir="tests/test_internal/fixtures/tester_results"
        )

    context.start_time = 0
    context.num_of_instances = 100

    return context

def get_base_parsed_data(base_context: AlgTesterContext, algorithm: Algorithm) -> Dict[str, object]:
    dummy_data = dict()
    dummy_data["output_filename"] = "output_filename"
    dummy_data["algorithm_name"] = algorithm.get_name()
    dummy_data["algorithm"] = algorithm

    return dummy_data

def _dummy_perform_algorithm(context: AlgTesterContext, parsed_data: Dict[str, object]) -> Dict[str, object]:
    return parsed_data

def create_dummy_algorithm(columns: List[str] = ["id", "algorithm_name"], name: str = "DummyAlgorithm", perform_func = _dummy_perform_algorithm):
    class DummyAlgorithm(Algorithm):

        def get_name(self) -> str:
            return name 

        def get_columns(self, show_time: bool = True) -> List[str]:
            return columns

        def perform_algorithm(self, context: AlgTesterContext, parsed_data: Dict[str, object]) -> Dict[str, object]:
            return perform_func(context, parsed_data)

    return DummyAlgorithm()

def create_dummy_parser(name: str = "DummyParser", write_result: bool = False):
    class DummyParser(Parser):

        def get_name(self) -> str:
            return name

        def get_output_file_name(self, context: AlgTesterContext, input_file: IO, click_args: Dict[str, object]) -> str:
            input_file_name: str = input_file.name.split("/")[-1]

            return input_file_name.replace(".dat", f'_{click_args["algorithm_name"]}_sol.dat')

        def get_instance_identifier(self, instance_data: Dict[str, object]) -> str:
            return ",".join([instance_data["id"], instance_data["item_count"]])

        def get_num_of_instances(self, context: AlgTesterContext, input_file: IO) -> int:
            for index, _ in enumerate(input_file):
                pass

            return index + 1

        def get_next_instance(self, input_file: IO) -> Dict[str, object]:
            instance: str = input_file.readline()

            if instance is None or instance == "":
                return None

            values: List[str] = instance.split(" ")
            id, count, capacity = int(values.pop(0)), int(values.pop(0)), int(values.pop(0))
            it = iter(values)
            things = [(pos, int(weight), int(cost)) for pos, (weight, cost) in enumerate(list(zip(it, it)))]

            parsed_data = {
                "id": id,
                "item_count": count,
                "capacity": capacity,
                "things": things
            }

            return parsed_data

        def write_result_to_file(self, output_file: IO, data: Dict[str, object]):
            if write_result:
                columns: List[str] = data["algorithm"].get_columns()

                if data.get("things") is not None:
                    data["things"] = "".join(map(str, data["things"]))
                
                output_data = [data.get(column) for column in columns]
                
                output: str = f'{" ".join(map(str, output_data))}'
                output_file.write(f'{output}\n')
                output_file.flush()

    return DummyParser()