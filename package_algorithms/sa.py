from typing import List, Dict
import numpy as np
from algorithm_tester.tester_dataclasses import Algorithm, DynamicClickOption
from package_algorithms.alg_dataclasses import Task, Thing

class SimulatedAnnealing(Algorithm):
    """ Uses Simulated annealing algorithm. """

    def required_click_params(self) -> List[DynamicClickOption]:
        init_temp = DynamicClickOption(name="init_temperature", data_type=float, short_opt="", long_opt="--init-temperature", 
            required=True, doc_help="A float number from interval (0; +inf). Represents the starting temperature of SA.")
        cooling = DynamicClickOption(name="cooling", data_type=float, short_opt="", long_opt="--cooling", 
            required=True, doc_help="A float number from interval (0; 1]. Represents the cooling coefficient of SA. Usage: temperature1 = temperature0 * cooling")
        min_temp = DynamicClickOption(name="min_temperature", data_type=float, short_opt="", long_opt="--min-temperature", 
            required=True, doc_help="A float number from interval (0; +inf). Represents the minimum temperature of SA. The algorithm ends when this or lower temperature is achieved.")
        cycles = DynamicClickOption(name="cycles", data_type=int, short_opt="", long_opt="--cycles", 
            required=True, doc_help="An int number from interval (0; +inf). Represents the number of internal cycles of SA that are done before cooling occurs.")
        
        return [init_temp, cooling, min_temp, cycles]

    def get_name(self) -> str:
        return "SA"

    def get_columns(self, show_time: bool = True) -> List[str]:
        columns: List[str] = [
            "id",
            "item_count",
            "algorithm_name",
            "init_temperature",
            "cooling",
            "min_temperature",
            "cycles",
            "found_value",
            "elapsed_configs",
            "elapsed_time",
            "things"
        ]

        return columns
 
    def perform_algorithm(self, parsed_data: Dict[str, object]) -> Dict[str, object]:
        # FIXME: Implement
        # FIXME: Použít Task? - Spíš ne, vytvořit vlastní třídu pro uložení zde.
        # task: Task = Task(parsed_data=parsed_data)
        # task.things = sorted(task.things, key=lambda thing: thing.cost/thing.weight, reverse=True)

        # parsed_data.update({
        #     "max_value": result.max_value,
        #     "elapsed_configs": config_ctr.value,
        #     "things": result.things
        # })

        print("Test")

        return parsed_data