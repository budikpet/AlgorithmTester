cimport numpy
cimport cython

ctypedef numpy.int64_t TYPE

cdef class SolutionSA():
    cdef long[:] solution
    cdef int sum_cost
    cdef int sum_weight

    def __cinit__(self, numpy.ndarray[TYPE, ndim=1] solution, int sum_cost, int sum_weight):
        self.solution = solution
        self.sum_cost = sum_cost
        self.sum_weight = sum_weight
    
    def __getitem__(self, int key):
        return self.solution[key]
    
    def __setitem__(self, int key, int value):
        self.solution[key] = value

    cdef copy(self, SolutionSA other):
        self.solution = other.solution.copy()
        self.sum_cost = other.sum_cost
        self.sum_weight = other.sum_weight

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexes checking
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
cpdef (int, int) get_new_neighbour(long[:] solution, int cost_sum, int weight_sum, int index, int capacity, int count, long[:] costs, long[:] weights):
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

# cpdef (long[:], int, int) get_solution(long[:] solution, int sum_cost, int sum_weight, float init_temperature, float min_temperature, float cooling_coef, int cycles, long[:] costs, long[:] weights):
#     print