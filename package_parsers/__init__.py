from package_parsers.knapsack_parser import KnapsackParser
from package_parsers.sat_parser import SATParser

__plugins__ = [KnapsackParser, SATParser]
__all__ = [plugin.__name__ for plugin in __plugins__]