from package_algorithms.bb import BranchBound, SortedBranchBound
from package_algorithms.dp import DynamicProgramming, DynamicProgramming_Weight
from package_algorithms.basic import BruteForce, Greedy
from package_algorithms.sa import SimulatedAnnealing
from package_algorithms.sa_penalty import SimulatedAnnealingPenalty
from package_algorithms.sa_old import SimulatedAnnealing_OLD

__plugins__ = [BranchBound, BruteForce, DynamicProgramming, DynamicProgramming_Weight, Greedy, SortedBranchBound, SimulatedAnnealing, SimulatedAnnealingPenalty, SimulatedAnnealing_OLD]
__all__ = [plugin.__name__ for plugin in __plugins__]