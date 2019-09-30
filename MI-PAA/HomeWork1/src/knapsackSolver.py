import click
import os
from myDataClasses import Task, Solution
import solverStrategy

class Context():

    def __init__(self, strategy):
        self.strategy = strategy

    def solve(self, task: Task):
        self.strategy.solve(task)

@click.command()
@click.option("--dataFile", type=click.File("r"), required=True)
def knapsackSolver(datafile):
    data = datafile.readline()
    context = Context(solverStrategy.BranchBorder())

    while data:
        values = data.split(" ")
        task = Task(id=values.pop(0), count=values.pop(0), capacity=values.pop(0), minValue=values.pop(0), thingValues=values)

        context.solve(task)

        data = datafile.readline()

    print


if __name__ == "__main__":
    knapsackSolver()    # pylint: disable=no-value-for-parameter