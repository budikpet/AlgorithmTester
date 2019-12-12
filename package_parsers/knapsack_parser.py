from typing import Dict, List
from algorithm_tester.tester_dataclasses import Parser

class KnapsackParser(Parser):

    def get_name(self) -> str:
        return "KnapsackParser"

    def get_output_file_name(self, click_args: Dict[str, object]) -> str:
        res: str = "tmp"

        return res

    def get_next_instance(self) -> Dict[str, object]:
        instance: str = self.input_file.readline()

        if instance is None or instance == "":
            return None

        solution: Dict[str, object] = None
        values: List[str] = instance.split(" ")
        id, count, capacity = int(values.pop(0)), int(values.pop(0)), int(values.pop(0))
        it = iter(values)
        things = [(pos, int(weight), int(cost)) for pos, (weight, cost) in enumerate(list(zip(it, it)))]

        parsed_data = {
            "id": id,
            "item_count": count,
            "capacity": capacity,
            "things": things,
            "elapsed_time": 0.0
        }

        return parsed_data