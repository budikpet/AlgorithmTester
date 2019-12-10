import pkg_resources
import sys, inspect
from typing import Dict, List
from algorithm_tester.algorithms import Algorithm

"""
This module should be used to automatically retrieve plugins (Algorithm classes, Parser classes) from setup.py entrypoints.

"""

__discovered_plugins = {
    entry_point.name: entry_point.load() for entry_point in pkg_resources.iter_entry_points('algorithm_tester.plugins')
}

def get_subclasses(package, parent_class: type) -> List[type]:
    predicate = lambda member: inspect.isclass(member) and issubclass(member, parent_class) and member.__name__ != parent_class.__name__
    
    # clsmembers = inspect.getmembers(sys.modules[name], predicate=predicate)
    return list(filter(predicate, package.__plugins__))

def get_plugins() -> Dict[str, List[type]]:
    package_algorithms = __discovered_plugins["algorithms"]
    package_parsers = __discovered_plugins["parsers"]

    result: Dict[str, List[type]] = {
        "algorithms": get_subclasses(package_algorithms, Algorithm),
        "parsers": get_subclasses(package_parsers, Algorithm)   #FIXME: Add parser interface
    }

    # for clsmember in result["algorithms"]:
    #     instance: Algorithm = clsmember()
    #     print(instance.get_column_descriptions())

get_plugins()