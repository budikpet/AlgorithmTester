from typing import Dict
from algorithm_tester.tester_dataclasses import Parser

class KnapsackParser(Parser):

    def get_name(self) -> str:
        return "KnapsackParser"

    def get_output_file_name(click_args: Dict[str, object]) -> str:
        res: str = "tmp"

        return res