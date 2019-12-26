import numpy as np
cimport numpy as np
cimport cython
from math import exp

ctypedef np.int64_t TYPE

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexes checking
@cython.initializedcheck(False)
cdef (int, int) repair_solution(long[:] solution, int cost_sum, int weight_sum, int capacity, int count, long[:] costs, long[:] weights) nogil:
    """
    If the weight_sum exceeds capacity, this function repairs it. 
    
    Removes items until weight_sum <= capacity in order from the lowest cost/weight to the highest.
    
    Returns:
        tuple -- A tuple (cost_sum, weight_sum) of modified values.
    """
    
    cdef int index
    
    if weight_sum <= capacity:
        return cost_sum, weight_sum
    
    for index in range(count, -1, -1):
        if solution[index] == 1:
            solution[index] = 0
            cost_sum -= costs[index]
            weight_sum -= weights[index]

            if weight_sum <= capacity:
                return cost_sum, weight_sum

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexes checking
@cython.initializedcheck(False)
cdef (int, int) get_new_neighbour(long[:] solution, int cost_sum, int weight_sum, int index, int capacity, int count, long[:] costs, long[:] weights):
    cdef int new_value 

    new_value = (solution[index] + 1) % 2
    solution[index] = new_value

    if new_value == 1:
        cost_sum += costs[index]
        weight_sum += weights[index]
        cost_sum, weight_sum = repair_solution(solution, cost_sum, weight_sum, capacity, count, costs, weights)
    else:
        cost_sum -= costs[index]
        weight_sum -= weights[index]

    return cost_sum, weight_sum

# while curr_temp > task.min_temp:
#     rand_indexes: np.ndarray = np.random.randint(0, task.count-1, size=task.cycles, dtype=int)
#     rand_exp_predicates: np.ndarray = np.random.uniform(size=task.cycles)
#     for cycle in range(task.cycles):
#         sol_cntr += 1

#         # Try neighbour solution
#         csa.get_new_neighbour(neighbour_sol.solution, neighbour_sol.sum_cost, neighbour_sol.sum_weight, 
#             index=rand_indexes[cycle], capacity=task.capacity, count=task.count, costs=costs, weights=weights)
#         neighbour_fitness: float = self.get_fitness(task, neighbour_sol)

#         if neighbour_fitness > best_fitness:
#             # Neighbour solution is better, accept it
#             best_fitness = neighbour_fitness
#             best_sol.copy(neighbour_sol)

#         elif exp( (neighbour_fitness - best_fitness) / curr_temp) >= rand_exp_predicates[cycle]:
#             # Simulated Annealing condition. 
#             # Enables us to accept worse solution with a certain probability
#             best_fitness = neighbour_fitness
#             best_sol.copy(neighbour_sol)

#         else:
#             # Change the solution back
#             neighbour_sol.copy(best_sol)
#         print

#     curr_temp *= task.cooling_coefficient

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexes checking
@cython.initializedcheck(False)
cpdef (int, int, int) get_solution(long[:] solution, int sum_cost, int sum_weight, float init_temp, float min_temp, float cooling_coef, int cycles, int capacity, long[:] costs, long[:] weights):
    cdef long[:] best_sol, neighbour_sol, rand_indexes
    cdef double[:] rand_exp_predicates
    cdef int count, sol_cntr, best_cost, best_weight, neighbour_cost, neighbour_weight
    cdef float curr_temp

    best_cost, best_weight, neighbour_cost, neighbour_weight = sum_cost, sum_weight, sum_cost, sum_weight
    sol_cntr = 0
    count = solution.size
    curr_temp = init_temp
    
    best_sol = solution.copy()
    neighbour_sol = solution.copy()

    while curr_temp > min_temp:
        rand_indexes = np.random.randint(0, count-1, size=cycles, dtype=int)
        rand_exp_predicates = np.random.uniform(size=cycles)
        for cycle in range(cycles):
            sol_cntr += 1

            # Try neighbour solution
            get_new_neighbour(neighbour_sol, neighbour_cost, neighbour_weight,
                index=rand_indexes[cycle], 
                capacity=capacity, count=count, costs=costs, weights=weights)

            if neighbour_cost > best_cost:
                # Neighbour solution is better, accept it
                best_sol = neighbour_sol.copy()
                best_cost = neighbour_cost
                best_weight = neighbour_weight

            elif exp( (neighbour_cost - best_cost) / curr_temp) >= rand_exp_predicates[cycle]:
                # Simulated Annealing condition. 
                # Enables us to accept worse solution with a certain probability
                best_sol = neighbour_sol.copy()
                best_cost = neighbour_cost
                best_weight = neighbour_weight

            else:
                # Change the solution back
                neighbour_sol = best_sol.copy()
                neighbour_cost = best_cost
                neighbour_weight = best_weight
            print

        curr_temp *= cooling_coef

    return best_cost, best_weight, sol_cntr