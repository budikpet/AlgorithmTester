import pkg_resources
import sys, inspect
from algorithm_tester.algorithms import Algorithm

"""
This module should be used to automatically retrieve plugins (Algorithm classes, Parser classes) from setup.py entrypoints.

"""

def algorithm_subclasses(plugins_package):
    predicate = lambda member: inspect.isclass(member) and issubclass(member, Algorithm) and member.__name__ != Algorithm.__name__
    
    # clsmembers = inspect.getmembers(sys.modules[name], predicate=predicate)
    return list(filter(predicate, plugins_package.__plugins__))

discovered_plugins = {
    entry_point.name: entry_point.load() for entry_point in pkg_resources.iter_entry_points('myapp.plugins')
}

plugins_package = discovered_plugins["a"]

clsmembers = algorithm_subclasses(plugins_package)

for clsmember in clsmembers:
    instance: Algorithm = clsmember()
    print(instance.get_column_descriptions())