import pkg_resources
import sys, inspect
from algorithm_tester.algorithms import Algorithm

"""
This module should be used to automatically retrieve plugins (Algorithm classes, Parser classes) from setup.py entrypoints.

"""

def print_Algorithm_subclasses(name: str):
    predicate = lambda member: inspect.isclass(member) and issubclass(member, Algorithm) and member.__name__ != Algorithm.__name__
    
    clsmembers = inspect.getmembers(sys.modules[name], predicate=predicate)
    for clsmember in clsmembers:
        print(clsmember)

    # for name, obj in inspect.getmembers(sys.modules[name]):
    #     if inspect.isclass(obj):
    #         print(obj)

discovered_plugins = {
    entry_point.name: entry_point.load() for entry_point in pkg_resources.iter_entry_points('myapp.plugins')
}

plug_module = discovered_plugins["a"]
test2 = plug_module.BruteForce_Outer()
print(discovered_plugins)