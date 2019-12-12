from algorithm_tester.abstracts import Algorithm
from package_algorithms.bb import BranchBound, SortedBranchBound
from package_algorithms.dp import DynamicProgramming, DynamicProgramming_Weight
from package_algorithms.basic import BruteForce, Greedy

__plugins__ = [BranchBound, BruteForce, DynamicProgramming, DynamicProgramming_Weight, Greedy, SortedBranchBound]
__all__ = [plugin.__name__ for plugin in __plugins__]