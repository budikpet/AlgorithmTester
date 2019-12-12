from package_parsers.knapsack_parser import KnapsackParser

__plugins__ = [KnapsackParser]
__all__ = [plugin.__name__ for plugin in __plugins__]