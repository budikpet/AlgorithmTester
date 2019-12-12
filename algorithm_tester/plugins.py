import pkg_resources
import sys, inspect
from typing import Dict, List, Set
from algorithm_tester.tester_dataclasses import Algorithm, Parser, DynamicClickOption

"""
This module should be used to automatically retrieve plugins (Algorithm classes, Parser classes) from setup.py entrypoints.

"""

__discovered_plugins = {
    entry_point.name: entry_point.load() for entry_point in pkg_resources.iter_entry_points('algorithm_tester.plugins')
}

def get_subclasses(package, parent_class: type) -> List[type]:
    predicate = lambda member: inspect.isclass(member) and issubclass(member, parent_class) and member.__name__ != parent_class.__name__
    
    # clsmembers = inspect.getmembers(sys.modules[name], predicate=predicate)
    return [plugin() for plugin in package.__plugins__ if predicate(plugin)]

def get_plugins(key: str, parent_class: type) -> List[type]:
    package_algorithms = __discovered_plugins[key]

    subclasses = get_subclasses(package_algorithms, parent_class)
    return subclasses

class Plugins():

    def __init__(self):
        self.__algorithms: List[Algorithm] = get_plugins("algorithms", parent_class=Algorithm)
        self.__parsers: List[Parser] = get_plugins("parsers", parent_class=Parser)

    #################################################################################################
    #  ALGORITHMS                                                                                   #
    #################################################################################################

    def get_dynamic_options(self) -> List[DynamicClickOption]:
        options: Set[DynamicClickOption] = set("")
        for alg in self.__algorithms:
            params: List[DynamicClickOption] = alg.required_click_params()
            
            if params is not None:
                options.update(params)
        
        return list(options)

    def get_algorithms(self, with_names: List[str] = None) -> List[Algorithm]:
        if with_names is None:
            return self.__algorithms
        
        # Filter algorithms that match the given names

        return [alg for alg in self.__algorithms if alg.get_name() in with_names]

    def get_algorithm(self, name: str) -> Algorithm:
        return [alg for alg in self.__algorithms if alg.get_name() == name][0]
    
    def get_algorithm_names(self) -> List[str]:
        return [alg.get_name() for alg in self.__algorithms]

    #################################################################################################
    #  PARSERS                                                                                      #
    #################################################################################################

    def get_parser(self, name: str) -> Parser:
        return [parser for parser in self.__parsers if parser.get_name() == name][0]
    
    def get_parser_names(self) -> List[str]:
        return [parser.get_name() for parser in self.__parsers]

plugins: Plugins = Plugins()