cimport numpy as np
cimport cython

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexes checking
@cython.initializedcheck(False)
@cython.cdivision(True)
cdef (void) add_invalid_literals(long[:] invalid_literals_per_var, long[:] invalid_literals_per_var_helper):
    cdef size_t i, I
    I = invalid_literals_per_var.shape[0]

    for i in range(I):
        invalid_literals_per_var[i] += invalid_literals_per_var_helper[i]

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexes checking
@cython.initializedcheck(False)
@cython.cdivision(True)
cpdef (int, bint) check_validity(long[:] invalid_literals_per_var, long[:] invalid_literals_per_var_helper, long[:, :] clauses, long[:] solution, int num_of_clauses):
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
        invalid_literals_per_var_helper[:] = 0

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
                    invalid_literals_per_var_helper[index] += 1
        
        if is_satisfied:
            # Last clause was satisfied
            num_of_satisfied_clauses += 1
        else:
            # Last clause was not satisfied, add it's variables to invalid_literals_per_var
            add_invalid_literals(invalid_literals_per_var, invalid_literals_per_var_helper)
    
    is_valid = num_of_clauses == num_of_satisfied_clauses

    return (num_of_satisfied_clauses, is_valid)