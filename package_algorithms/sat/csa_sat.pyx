cimport numpy as np
cimport cython

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexes checking
@cython.initializedcheck(False)
@cython.cdivision(True)
cpdef (int, bint) check_validity(long[:] invalid_literals_per_var, long[:, :] clauses, long[:] solution, int num_of_clauses):
    cdef int num_of_satisfied_clauses = 0
    cdef bint is_satisfied = False
    cdef bint is_valid = False
    cdef int value, index, sol_value

    # Go through the clauses memoryview using indexes
    cdef size_t i, j, I, J
    I = clauses.shape[0]
    J = clauses.shape[1]

    invalid_literals_per_var[:] = 0

    # Check all variables of all clauses
    for i in range(I):
        is_satisfied = False

        for j in range(J):
            value = clauses[i, j]
            if value != 0:
                index = abs(value) - 1
                sol_value: int = solution[index]
                if (sol_value == 0 and value < 0) or (sol_value == 1 and value > 0):
                    # Clause satisfied
                    is_satisfied = True
                else: 
                    # Clause not satisfied
                    invalid_literals_per_var[index] += 1
        
        if is_satisfied:
            # Last clause was satisfied
            num_of_satisfied_clauses += 1
    
    is_valid = num_of_clauses == num_of_satisfied_clauses

    return (num_of_satisfied_clauses, is_valid)