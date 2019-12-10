from algorithm_tester.algorithms import Algorithm
from algorithm_tester.tester_dataclasses import Task, Solution, Thing, ConfigCounter, RecursiveResult

class BruteForce_Outer(Algorithm):
    """ Uses Brute force  """

    def get_name(self) -> str:
        return "BruteForce_Outer"

    def get_column_descriptions(self, show_time: bool = True):
        res: str = super().get_column_descriptions(show_time=show_time)
        res[-2] = "|replaced|"

        return res
    
    def perform_algorithm(self, task: Task) -> Solution:
        # Sort things by cost/weight comparison
        task.things = sorted(task.things, key=lambda thing: thing.cost/thing.weight, reverse=True)

        return Solution(task=task, max_value=10, 
            elapsed_configs=-1, things=list())