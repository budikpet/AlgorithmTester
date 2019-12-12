import os
import timeit
from typing import Dict
from algorithm_tester.abstracts import TesterContext
from algorithm_tester.plugins import plugins

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

def get_instance_file_results(datafile, algorithm: str, check_time: bool, time_retries: int, other_options: Dict[str, object] = None):
    data = datafile.readline()
    context = TesterContext(plugins.get_algorithm(name=algorithm))

    while data:
        solution: Dict[str, object] = None
        values = data.split(" ")
        id, count, capacity = int(values.pop(0)), int(values.pop(0)), int(values.pop(0))
        it = iter(values)
        things = [(pos, int(weight), int(cost)) for pos, (weight, cost) in enumerate(list(zip(it, it)))]

        parsed_data = {
            "id": id,
            "algorithm_name": algorithm,
            "item_count": count,
            "capacity": capacity,
            "things": things,
            "elapsed_time": 0.0
        }
        
        if other_options is not None:
            parsed_data.update(other_options)

        if check_time:
            # Use timeit to get time
            t = timeit.Timer(lambda: context.perform_algorithm(parsed_data))
            elapsed_time, solution = t.timeit(number=time_retries)
            solution["elapsed_time"] = round((elapsed_time*1000)/time_retries, 10)   # Store in millis
        else:
            solution = context.perform_algorithm(parsed_data)

        yield solution

        data = datafile.readline()
    
    print