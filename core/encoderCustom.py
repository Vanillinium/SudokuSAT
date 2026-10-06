import math

# Binomal/Pairwise Encoding (to represent the problem)
# O(N^2)
def eoBinomal(clauses, vars, currTopVar):
    # ALO: Each square must contain a value
    # (x1 v x2 v ...)
    clauses.append(vars)

    #AMO: Each square can only contain a single value
    # (-x1 v -x2 v ...)
    for i in range(len(vars)):
        for j in range(i + 1, len(vars)):
            clauses.append([-vars[i], -vars[j]])

    return currTopVar


# Binary/Bitwise Encoding
# O(NlogN)
def binaryAMO(clauses, vars, currTopVar):
    m = len(vars)

    if m <= 1: return currTopVar

    auxNum = math.ceil(math.log2(m))
    auxVars = [currTopVar + i + 1 for i in range(auxNum)]
    newTopVar = currTopVar + auxNum

    for i, var in enumerate(vars):
        for k in range(auxNum):
            bit = (i >> k) & 1 

            auxLit = auxVars[k] if bit == 1 else -auxVars[k]
            clauses.append([-var, auxLit])

    return newTopVar


def eoBinary(clauses, vars, currTopVar):
    # ALO: Each square must contain a value
    # (x1 v x2 v ...)
    clauses.append(vars)

    #AMO: Each square can only contain a single value
    # (-x1 v -x2 v ...)
    newTopVar = binaryAMO(clauses, vars, currTopVar)

    return newTopVar