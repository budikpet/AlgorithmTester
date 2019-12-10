from myapp_plugin_a.algorithms_outer import BruteForce_Outer
from myapp_plugin_a.algorithms_outer2 import Greedy_Outer
from algorithm_tester.algorithms import Algorithm

__plugins__ = [BruteForce_Outer, Greedy_Outer]
__all__ = [plugin.__name__ for plugin in __plugins__]