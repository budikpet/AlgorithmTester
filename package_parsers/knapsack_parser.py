from typing import Dict
from algorithm_tester.abstracts import Parser

class KnapsackParser(Parser):

    def get_name(self) -> str:
        return "KnapsackParser"

    def get_output_file_name(solution_data: Dict[str, object]) -> str:
        res: str = "tmp"

        return res