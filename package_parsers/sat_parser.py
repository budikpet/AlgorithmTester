from typing import Dict, List, IO
import re
import numpy as np
from algorithm_tester_common.tester_dataclasses import Parser, AlgTesterContext

class SATParser(Parser):
    """
    Parses input files that were generated by the provided MI-PAA generator.
    """

    def get_name(self) -> str:
        return "SATParser"

    def get_output_file_name(self, context: AlgTesterContext, input_file: IO, click_args: Dict[str, object]) -> str:
        input_file_name: str = input_file.name.split("/")[-1]

        return input_file_name.replace(".mwcnf", f'_{click_args["algorithm_name"]}_sol.mwcnf')

    def get_next_instance(self, input_file: IO) -> Dict[str, object]:
        clauses: np.ndarray
        weights: np.ndarray
        num_of_vars, num_of_clauses = 0, 0
        output_filename: str

        last_clause: int = 0
        
        line = input_file.readline()
        while line is not None:
            line = re.sub('\s+', ' ', line).strip()
            if re.search("^ *c SAT instance", line) is not None:
                # Output file line
                split = line.split(" ")
                output_filename = split[-1].split("/")[-1].replace(".dat", "")
                print
            elif re.search("^ *p", line) is not None:
                # Information line
                split = line.split(" ")
                num_of_vars, num_of_clauses = int(split[2]), int(split[3])
                clauses = np.zeros(shape=(num_of_clauses, num_of_vars), dtype=int)
                weights = np.zeros(shape=num_of_vars, dtype=int)
            elif re.search("^ *w", line) is not None:
                # Weights line
                split = line.split(" ")[1:-1]
                for index, num in enumerate(split):
                    weights[index] = int(num)
            elif re.search("^ *0$", line) is not None:
                # Stop line
                break
            elif re.search("^ *-*[0-9]+", line) is not None:
                # Clause line
                split = line.split(" ")[:-1]
                for value in split:
                    value = int(value)
                    clauses[last_clause][abs(value) - 1] = value
                last_clause += 1

            line = input_file.readline()        

        parsed_data = {
            "num_of_vars": num_of_vars,
            "num_of_clauses": num_of_clauses,
            "clauses": clauses,
            "weights": weights,
            "output_filename": output_filename
        }

        return parsed_data

    def write_result_to_file(self, output_file: IO, data: Dict[str, object]):
        columns: List[str] = data["algorithm"].get_columns()
        
        output_data = [data.get(column) for column in columns]
        
        output: str = f'{" ".join(map(str, output_data))}'
        output_file.write(f'{output}\n')