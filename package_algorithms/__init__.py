from package_algorithms.knapsack.bb import BranchBound, SortedBranchBound
from package_algorithms.knapsack.dp import DynamicProgramming, DynamicProgramming_Weight
from package_algorithms.knapsack.basic import BruteForce, Greedy
from package_algorithms.knapsack.sa import SimulatedAnnealing
from package_algorithms.knapsack.sa_penalty import SimulatedAnnealingPenalty
from package_algorithms.knapsack.sa_old import SimulatedAnnealing_OLD
from package_algorithms.sat.sa_sat_v1 import SimulatedAnnealing_SAT_V1
from package_algorithms.sat.sa_sat_v2 import SimulatedAnnealing_SAT_V2
from package_algorithms.sat.sa_sat_v3 import SimulatedAnnealing_SAT_V3

# __plugins__ = [BranchBound, BruteForce, DynamicProgramming, DynamicProgramming_Weight, Greedy, SortedBranchBound, SimulatedAnnealing, SimulatedAnnealingPenalty, SimulatedAnnealing_OLD]
__plugins__  = [SimulatedAnnealing_SAT_V1, SimulatedAnnealing_SAT_V2, SimulatedAnnealing_SAT_V3]
__all__ = [plugin.__name__ for plugin in __plugins__]