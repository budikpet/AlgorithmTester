import click
import os
from myDataClasses import Task, Solution
import solverStrategy

@click.command()
@click.option("--dataFile", type=click.File("r"), required=True)
def knapsackSolver(datafile):
    data = datafile.readline()
    context = solverStrategy.Context(solverStrategy.BranchBorder())
    solutions = list()

    while data:
        values = data.split(" ")
        task = Task(id=values.pop(0), count=values.pop(0), capacity=values.pop(0), minValue=values.pop(0), thingValues=values)

        solution = context.solve(task)
        print(solution)
        solutions.append(solution)

        data = datafile.readline()

    return solutions


if __name__ == "__main__":
    knapsackSolver()    # pylint: disable=no-value-for-parameter