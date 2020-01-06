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
    cdef long[:] clause
    cdef int value, index

    invalid_literals_per_var[:] = 0

    for clause in clauses:
        is_satisfied = False

        for value in clause:
            if value != 0:
                index = abs(value) - 1
                sol_value: int = solution[index]
                if (sol_value == 0 and value < 0) or (sol_value == 1 and value > 0):
                    # Clause satisfied
                    is_satisfied = True
                else: 
                    invalid_literals_per_var[index] += 1
        
        if is_satisfied:
            # Last clause was satisfied
            num_of_satisfied_clauses += 1
    
    is_valid = num_of_clauses == num_of_satisfied_clauses

    return (num_of_satisfied_clauses, is_valid)