import os
import timeit
from algorithm_tester.mydataclasses import Task, Solution, Thing
from algorithm_tester.solver_strategy import Strategies, Context

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

def knapsack_solver(datafile, strategy: str, check_time: bool, time_retries: int, relative_mistake: float = None):
    data = datafile.readline()
    context = Context(Strategies[strategy].value)

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

        yield solution

        data = datafile.readline()
    
    print