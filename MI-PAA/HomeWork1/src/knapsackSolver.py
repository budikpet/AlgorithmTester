import click
import os
from myDataClasses import Task, Solution, Thing
import solverStrategy
from solverStrategy import Strategies, Modes

inputStrategies = [strategy.name for strategy in Strategies]
inputModes = [mode.name for mode in Modes]

@click.command()
@click.option("--dataFile", type=click.File("r"), required=True)
@click.option("-s", "--strategy", type=click.Choice(inputStrategies), default=inputStrategies[0])
@click.option("--mode", type=click.Choice(inputModes), default=inputModes[0])
def knapsackSolver(datafile, strategy, mode):
    data = datafile.readline()
    context = solverStrategy.Context(Modes[mode], Strategies[strategy].value)
    solutions = list()

    while data:
        values = data.split(" ")
        id, count, capacity, minValue = int(values.pop(0)), int(values.pop(0)), int(values.pop(0)), int(values.pop(0))
        it = iter(values)
        things = [Thing(pos, int(weight), int(cost)) for pos, (weight, cost) in enumerate(list(zip(it, it)))]

        task = Task(id=id, count=count, capacity=capacity, minValue=minValue, things=things)

        solution = context.solve(task)
        
        # Print necessery for unit tests
        print(solution)
        solutions.append(solution)

        data = datafile.readline()

    return solutions


if __name__ == "__main__":
    knapsackSolver()    # pylint: disable=no-value-for-parameter