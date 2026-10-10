import math

# Binomal/Pairwise Encoding (to represent the problem)
# O(N^2)
def amoBinomal(clauses, vars, currTopVar):
    for i in range(len(vars)):
        for j in range(i + 1, len(vars)):
            clauses.append([-vars[i], -vars[j]])

    return currTopVar

def eoBinomal(clauses, vars, currTopVar):
    # ALO: Each square must contain a value
    # (x1 v x2 v ...)
    clauses.append(vars)
    
    #AMO: Each square can only contain a single value
    # (-x1 v -x2 v ...)
    return amoBinomal(clauses, vars, currTopVar)


# Binary/Bitwise Encoding
# O(NlogN)
def amoBinary(clauses, vars, currTopVar):
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
    newTopVar = amoBinary(clauses, vars, currTopVar)

    return newTopVar


# Product Encoding
# O(sqrtN)
def amoProduct(clauses, vars, currTopVar):
    m = len(vars)
    if m <= 1: return currTopVar

    # Turning the clauses into a p x q matrix
    p = math.ceil(math.sqrt(m))
    q = math.ceil(m / p)

    varsR = [currTopVar + i + 1 for i in range(p)]
    varsC = [currTopVar + p + j + 1 for j in range(q)]
    
    currTopVar = currTopVar + p + q

    if len(varsR) > 10:
        currTopVar = amoBinary(clauses, varsR, currTopVar)
    else:
        currTopVar = amoBinomal(clauses, varsR, currTopVar)

    if len(varsC) > 10:
        currTopVar = amoBinary(clauses, varsC, currTopVar)
    else:
        currTopVar = amoBinomal(clauses, varsC, currTopVar)

    x = 0
    for i in range(len(varsR)):
        for j in range(len(varsC)):
            if x < m:
                var = vars[x]
                clauses.append([-var, varsR[i]])
                clauses.append([-var, varsC[j]])
            
                x += 1

            else: break

        if x >= m: break

    return currTopVar

def eoProduct(clauses, vars, currTopVar):
    # ALO: Each square must contain a value
    # (x1 v x2 v ...)
    clauses.append(vars)

    #AMO: Each square can only contain a single value
    # (-x1 v -x2 v ...)
    newTopVar = amoProduct(clauses, vars, currTopVar)

    return newTopVar









