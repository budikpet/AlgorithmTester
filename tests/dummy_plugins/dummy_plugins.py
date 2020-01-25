from typing import List, Dict, IO
import time
from algorithm_tester_common.tester_dataclasses import Algorithm, Parser, Communicator, AlgTesterContext

class DummyAlgorithm(Algorithm):

    def get_name(self) -> str:
        return "DummyAlgorithm" 

    def get_columns(self, show_time: bool = True) -> List[str]:
        return ["index", "name"]

    def perform_algorithm(self, context: AlgTesterContext, parsed_data: Dict[str, object]) -> Dict[str, object]:
        time.sleep(0.5)
        parsed_data.update({
            "index": int(parsed_data["id"]),
            "name": f'Test_{parsed_data["item_count"]}'
        })

        return parsed_data

class DummyParser(Parser):
    """
    Parses input files that were generated by the provided MI-PAA generator.
    """

    def get_name(self) -> str:
        return "DummyParser"

    def get_output_file_name(self, context: AlgTesterContext, input_file: IO, click_args: Dict[str, object]) -> str:
        input_file_name: str = input_file.name.split("/")[-1]

        return input_file_name.replace(".dat", f'_{click_args["algorithm_name"]}_sol.dat')

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
        columns: List[str] = data["algorithm"].get_columns()

        if data.get("things") is not None:
            data["things"] = "".join(map(str, data["things"]))
        
        output_data = [data.get(column) for column in columns]
        
        output: str = f'{" ".join(map(str, output_data))}'
        output_file.write(f'{output}\n')
        output_file.flush()