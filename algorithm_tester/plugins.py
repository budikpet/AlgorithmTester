import pkg_resources
import sys, inspect, os
from typing import Dict, List, Set
from configparser import ConfigParser
from algorithm_tester_common.tester_dataclasses import Algorithm, Parser, Communicator, DynamicClickOption

"""
This module should be used to automatically retrieve plugins (Algorithm, Parser and Communicators classes) from setup.py entrypoints.

"""

__discovered_plugins = {
    entry_point.name: entry_point.load() for entry_point in pkg_resources.iter_entry_points('algorithm_tester.plugins')
}

def get_subclasses(package, parent_class: type) -> List[type]:
    """
    Returns only plugin classes - classes that are provided in the package and are subclasses of the specified parent class.
    
    Args:
        package ([type]): Inspected package
        parent_class (type): Class the plugin must be subclass of.
    
    Returns:
        List[type]: All found plugin classes.
    """
    predicate = lambda member: inspect.isclass(member) and issubclass(member, parent_class) and member.__name__ != parent_class.__name__
    
    # clsmembers = inspect.getmembers(sys.modules[name], predicate=predicate)
    return [plugin() for plugin in package.__plugins__ if predicate(plugin)]

def get_plugins(key: str, parent_class: type) -> List[type]:
    """[summary]
    
    Arguments:
        key {str} -- Type of plugin the plugin.
        parent_class {type} -- Class the plugin must be subclass of.
    
    Returns:
        List[type] -- List of plugin classes of the required parent class that were provided using entrypoints.
    """
    package_algorithms = __discovered_plugins.get(key)

    if package_algorithms is None:
        return list()

    subclasses = get_subclasses(package_algorithms, parent_class)
    return subclasses

class Plugins():
    """
    Contains all found plugin classes.
    """

    def __init__(self):
        self.__algorithms: List[Algorithm] = get_plugins("algorithms", parent_class=Algorithm)
        self.__parsers: List[Parser] = get_plugins("parsers", parent_class=Parser)
        self.__communicators: List[Communicator] = get_plugins("communicators", parent_class=Communicator)

        # Internal communicators
        self.__add_slack_communicator()

    def __add_slack_communicator(self):
        """
        Adds Slack communicator to other communicators if slack_config environment variable is provided.

        Requires slack_config environment variable which contains a path to a valid slack configuration file.
        """
        if os.environ.get("slack_config") is None:
            return
        
        config_parser: ConfigParser = ConfigParser()
        with open(os.environ["slack_config"]) as config_file:
            config_parser.read_file(config_file)
        
        # Add slack config data to environment vars
        os.environ["slack_access_token"] = config_parser["auth"]["access_token"]
        os.environ["slack_channel_id"] = config_parser["channel"]["id"]
        os.environ["slack_bot_username"] = config_parser["channel"]["bot_username"]

        self.__communicators.extend(get_plugins("communicators_internal", parent_class=Communicator))
        print

    #################################################################################################
    #  ALGORITHMS                                                                                   #
    #################################################################################################

    def get_dynamic_options(self) -> List[DynamicClickOption]:
        """
        
        Returns:
            List[DynamicClickOption]: All dynamic options that are required by certain algorithms.
        """
        options: Set[DynamicClickOption] = set("")
        for alg in self.__algorithms:
            params: List[DynamicClickOption] = alg.required_click_params()
            
            if params is not None:
                options.update(params)
        
        return list(options)

    def get_algorithms(self, with_names: List[str] = None) -> List[Algorithm]:
        """
        Get instances of multiple algorithms.
        
        Args:
            with_names (List[str], optional): Names of required algorithms. Defaults to None.
        
        Returns:
            List[Algorithm]: Instances of required algorithms.
        """
        if with_names is None:
            return self.__algorithms
        
        # Filter algorithms that match the given names

        return [alg for alg in self.__algorithms if alg.get_name() in with_names]

    def get_algorithm(self, name: str) -> Algorithm:
        """
        Get an instance of an algorithm by name.
        
        Args:
            name (str): Name of the required algorithm.
        
        Returns:
            Algorithm: Instance of the required algorithm.
        """
        return [alg for alg in self.__algorithms if alg.get_name() == name][0]
    
    def get_algorithm_names(self) -> List[str]:
        """
        
        Returns:
            List[str]: Names of all available algorithms.
        """
        return [alg.get_name() for alg in self.__algorithms]

    #################################################################################################
    #  PARSERS                                                                                      #
    #################################################################################################

    def get_parser(self, name: str) -> Parser:
        """
        
        Args:
            name (str): Name of the required parser.
        
        Returns:
            Parser: Instance of the required parser.
        """
        return [parser for parser in self.__parsers if parser.get_name() == name][0]
    
    def get_parser_names(self) -> List[str]:
        """
        
        Returns:
            List[str]: Get names of all available parsers.
        """
        return [parser.get_name() for parser in self.__parsers]

    def get_parsers(self, with_names: List[str] = None) -> List[Parser]:
        """
        Get instances of multiple parsers.
        
        Args:
            with_names (List[str], optional): Names of required parsers. Defaults to None.
        
        Returns:
            List[Parser]: Instances of required algorithms.
        """
        if with_names is None:
            return self.__parsers
        
        # Filter algorithms that match the given names

        return [parser for parser in self.__parsers if parser.get_name() in with_names]

    #################################################################################################
    #  COMMUNICATORS                                                                                #
    #################################################################################################

    def get_communicators(self, with_names: List[str] = None) -> List[Communicator]:
        """
        Get instances of multiple communicators.
        
        Args:
            with_names (List[str], optional): Names of required communicators. Defaults to None.
        
        Returns:
            List[Communicator]: Instances of required communicators.
        """
        if with_names is None:
            return self.__communicators
        
        # Filter communicators that match the given names

        return [comm for comm in self.__communicators if comm.get_name() in with_names]

    def get_communicator(self, name: str) -> Communicator:
        """
        Get an instance of an communicator by name.
        
        Args:
            name (str): Name of the required communicator.
        
        Returns:
            Communicator: Instance of the required communicator.
        """
        return [comm for comm in self.__communicators if comm.get_name() == name][0]
    
    def get_communicator_names(self) -> List[str]:
        """
        
        Returns:
            List[str]: Names of all available communicators.
        """
        return [comm.get_name() for comm in self.__communicators]

plugins: Plugins = Plugins()