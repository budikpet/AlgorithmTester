import click
import os
import timeit
from myDataClasses import Task, Solution, Thing
from solverStrategy import Strategies, Context

# Enable timeit to return elapsed time and return value
new_template = """
def inner(_it, _timer{init}):
    {setup}
    _t0 = _timer()
    for _i in _it:
        ret_val = {stmt}
    _t1 = _timer()
    return _t1 - _t0, ret_val
"""
timeit.template = new_template

inputStrategies = [strategy.name for strategy in Strategies]

@click.command()
@click.option("--dataFile", type=click.File("r"), required=True)
@click.option("-e", "--relative-mistake", type=float, required=False, help="Useful only for FPTAS. A float number from interval (0; 100]. Represents highest possible mistake in percents.")
@click.option("-t", "--check-time", type=bool, default=True, help="Should the result also check elapsed time.")
@click.option("--time-retries", type=int, default=1, help="How many times should we retry if elapsed time is checked.")
@click.option("-s", "--strategy", type=click.Choice(inputStrategies), default=inputStrategies[0])
def knapsackSolver(datafile, relative_mistake: float, check_time: bool, time_retries: int, strategy):
    data = datafile.readline()
    context = Context(Strategies[strategy].value)
    solutions = list()

    if relative_mistake is not None:
        relative_mistake /= 100

    while data:
        values = data.split(" ")
        id, count, capacity = int(values.pop(0)), int(values.pop(0)), int(values.pop(0))
        it = iter(values)
        things = [Thing(pos, int(weight), int(cost)) for pos, (weight, cost) in enumerate(list(zip(it, it)))]

        task = Task(id=id, count=count, capacity=capacity, things=things, relative_mistake=relative_mistake)
        solution = None

        if check_time:
            # Use timeit to get time
            t = timeit.Timer(lambda: context.solve(task))
            elapsed_time, solution = t.timeit(number=time_retries)
            solution.elapsed_time = round((elapsed_time*1000)/time_retries, 10)   # Store in millis
        else:
            solution = context.solve(task)

        # Print necessery for unit tests
        print(solution)
        solutions.append(solution)

        data = datafile.readline()

    return solutions


if __name__ == "__main__":
    knapsackSolver()    # pylint: disable=no-value-for-parameter
