cimport numpy

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

# cpdef (numpy.ndarray[TYPE, ndim=1], int, int) get_initial_sol()