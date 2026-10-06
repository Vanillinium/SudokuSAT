# A Sudoku board is defined by N x N squares, creating N subboards of sqrtN x sqrtN.
# Each square is labeled as X(row, col, var).

# Translate square label to each ID on an 1D array.

import math

def generateVar(row, col, val, N):
    return (row - 1) * (N ** 2) + (col - 1) * N + val

# Given a grid/2D array of size N x N, translate the grid into a SAT problem.
def generateSudokuClauses(grid, eoFunc):
    """
    Translating the Sudoku problem into clauses needed for SAT solvers.

    :param grid: Sudoku board of N x N
    :param eoFunc: Function representing the Exactly-One requirement.
    :return: (clauses, totalVar)
    """

    N = len(grid)
    subN = int (N ** 0.5) #subgrids
    clauses = []
    currTopVar = N ** 3

    # Exactly 1 val in each (row, col) squares
    # (Xrc1 v Xrc2 v ... v Xrc9) ^ (-Xrc1 v -Xrc2) ^ ...
    for row in range(1, N + 1):
        for col in range(1, N + 1):
            cellVars = [generateVar(row, col, val, N) for val in range(1, N + 1)]
            currTopVar = eoFunc(clauses, cellVars, currTopVar)

    # Exactly 1 val for each value on each row
    # (Xr1v v Xr2v v ... v Xr9v) ^ (-Xr1v v -Xr2v) ^...
    for row in range(1, N + 1):
        for val in range(1, N + 1):
            colVars = [generateVar(row, col, val, N) for col in range(1, N + 1)]
            currTopVar = eoFunc(clauses, colVars, currTopVar)

    # Exactly 1 val for each value on each col
    # (X1cv v X2cv v ... v X9cv) ^ (-X1cv v -X2cv) ^...
    for col in range(1, N + 1):
        for val in range(1, N + 1):
            rowVars = [generateVar(row, col, val, N) for row in range(1, N + 1)]
            currTopVar = eoFunc(clauses, rowVars, currTopVar)

    # Exactly 1 val for each value on every subgrids
    # Per offsetR, offsetC:
    # (X11v v X12v v ... v XsqrtNsqrtNv) ^ (-X11v v X12v) ^ ...
    for offsetR in range(subN):
        for offsetC in range(subN):
            for val in range(1, N + 1):

                subVars = [generateVar(offsetR * subN + subR, offsetC * subN + subC, val, N)
                        for subR in range(1, subN + 1) 
                        for subC in range(1, subN + 1)]
                
                currTopVar = eoFunc(clauses, subVars, currTopVar)

    # Appending the given numbers
    for row in range(1, N + 1):
        for col in range(1, N + 1):
            givenVal = grid[row - 1][col - 1]

            if givenVal != 0:  # 0 -> empty square
                clauses.append([generateVar(row, col, givenVal, N)])

    return clauses, currTopVar

