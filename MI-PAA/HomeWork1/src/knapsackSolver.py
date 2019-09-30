import click
import os
from dataclasses import dataclass

@dataclass
class Task:
    id: int
    count: int
    capacity: int
    minValue: int
    things: [int]

@click.command()
@click.option("--dataFile", type=click.File("r"), required=True)
def knapsackSolver(datafile):
    data = datafile.readline()

    while data:
        values = data.split(" ")
        task = Task(id=values.pop(0), count=values.pop(0), capacity=values.pop(0), minValue=values.pop(0), things=values)

        data = datafile.readline()

    print


if __name__ == "__main__":
    knapsackSolver()    # pylint: disable=no-value-for-parameter