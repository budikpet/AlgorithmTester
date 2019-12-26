cimport numpy
cimport cython

ctypedef numpy.int64_t TYPE

# cdef class SolutionSA():
#     cdef numpy.int64_t[:] solution
#     cdef int sum_cost
#     cdef int sum_weight

#     def __cinit__(self, numpy.ndarray[TYPE, ndim=1] solution, int sum_cost, int sum_weight):
#         self.solution: np.ndarray = solution
#         self.sum_cost: int = sum_cost
#         self.sum_weight: int = sum_weight
    
    # def __getitem__(self, key):
    #     return self.solution[key]
    
    # def __setitem__(self, key, value):
    #     self.solution[key] = value

    # def copy(self, other):
    #     self.solution = other.solution.copy()
    #     self.sum_cost = other.sum_cost
    #     self.sum_weight = other.sum_weight

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexes checking
cpdef (int, int) repair_solution(long[:] solution, int cost_sum, int weight_sum, int capacity, int count, long[:] costs, long[:] weights):
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