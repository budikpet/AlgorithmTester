import click
import os
from myDataClasses import Task, Solution, Thing
import solverStrategy
from solverStrategy import Strategies

@click.command()
@click.option("--dataFile", type=click.File("r"), required=True)
@click.option("-s", "--strategy", type=click.Choice([Strategies.BruteForce.name, Strategies.BranchBorder.name]), default=Strategies.BruteForce.name)
def knapsackSolver(datafile, strategy):
    data = datafile.readline()
    context = solverStrategy.Context(Strategies[strategy].value)
    solutions = list()

    while data:
        values = data.split(" ")
        id, count, capacity, minValue = values.pop(0), values.pop(0), values.pop(0), values.pop(0)
        it = iter(values)
        things = [Thing(cost, weight) for (cost, weight) in list(zip(it, it))]

        task = Task(id=id, count=count, capacity=capacity, minValue=minValue, things=things)

        solution = context.solve(task)
        print(solution)
        solutions.append(solution)

        data = datafile.readline()

    return solutions


if __name__ == "__main__":
    knapsackSolver()    # pylint: disable=no-value-for-parameter