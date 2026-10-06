# A Sudoku board is defined by N x N squares, creating N subboards of sqrtN x sqrtN.
# Each square is labeled as X(row, col, var).

# Translate square label to each ID on an 1D array.

import math

def generateVar(row, col, val, N):
    return (row - 1) * (N ** 2) + (col - 1) * N + val


# Exactly One - Using Binary Encoding
# O(NlogN)
def atMostOne(clauses, vars, currTopVar):
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


def exactlyOne(clauses, vars, currTopVar):
    # ALO: Each square must contain a value
    # (x1 v x2 v ...)
    clauses.append(vars)

    #AMO: Each square can only contain a single value
    # (-x1 v -x2 v ...)
    newTopVar = atMostOne(clauses, vars, currTopVar)

    return newTopVar


# Given a grid/2D array of size N x N, translate the grid into a SAT problem.
def generateSudokuClauses(grid):
    N = len(grid)
    subN = int (N ** 0.5) #subgrids
    clauses = []

    currTopVar = N ** 3

    # Exactly 1 val in each (row, col) squares
    # (Xrc1 v Xrc2 v ... v Xrc9) ^ (-Xrc1 v -Xrc2) ^ ...
    for row in range(1, N + 1):
        for col in range(1, N + 1):
            cellVars = [generateVar(row, col, val, N) for val in range(1, N + 1)]
            currTopVar = exactlyOne(clauses, cellVars, currTopVar)

    # Exactly 1 val for each value on each row
    # (Xr1v v Xr2v v ... v Xr9v) ^ (-Xr1v v -Xr2v) ^...
    for row in range(1, N + 1):
        for val in range(1, N + 1):
            colVars = [generateVar(row, col, val, N) for col in range(1, N + 1)]
            currTopVar = exactlyOne(clauses, colVars, currTopVar)

    # Exactly 1 val for each value on each col
    # (X1cv v X2cv v ... v X9cv) ^ (-X1cv v -X2cv) ^...
    for col in range(1, N + 1):
        for val in range(1, N + 1):
            rowVars = [generateVar(row, col, val, N) for row in range(1, N + 1)]
            currTopVar = exactlyOne(clauses, rowVars, currTopVar)

    # Exactly 1 val for each value on every subgrids
    # Per offsetR, offsetC:
    # (X11v v X12v v ... v XsqrtNsqrtNv) ^ (-X11v v X12v) ^ ...
    for offsetR in range(subN):
        for offsetC in range(subN):
            for val in range(1, N + 1):

                subVars = [generateVar(offsetR * subN + subR, offsetC * subN + subC, val, N)
                        for subR in range(1, subN + 1) 
                        for subC in range(1, subN + 1)]
                
                currTopVar = exactlyOne(clauses, subVars, currTopVar)

    # Appending the given numbers
    for row in range(1, N + 1):
        for col in range(1, N + 1):
            givenVal = grid[row - 1][col - 1]

            if givenVal != 0:  # 0 -> empty square
                clauses.append([generateVar(row, col, givenVal, N)])

    return clauses, currTopVar

