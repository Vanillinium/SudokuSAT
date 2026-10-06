# A Sudoku board is defined by N x N squares, creating N subboards of sqrtN x sqrtN.
# Each square is labeled as X(row, col, var).

# Translate square label to each ID on an 1D array.
def generateVar(row, col, val, N):
    return (row - 1) * (N ** 2) + (col - 1) * N + val


# Exactly One - Using Binomal/Pairwise Encoding (to represent the problem)
# O(N^2)
def exactlyOne(clauses, vars):
    # ALO: Each square must contain a value
    # (x1 v x2 v ...)
    clauses.append(vars)

    #AMO: Each square can only contain a single value
    # (-x1 v -x2 v ...)
    for i in range(len(vars)):
        for j in range(i + 1, len(vars)):
            clauses.append([-vars[i], -vars[j]])


# Given a grid/2D array of size N x N, translate the grid into a SAT problem.
def generateSudokuClauses(grid):
    N = len(grid)
    subN = int (N ** 0.5) #subgrids
    clauses = []

    # Exactly 1 val in each (row, col) squares
    # (Xrc1 v Xrc2 v ... v Xrc9) ^ (-Xrc1 v -Xrc2) ^ ...
    for row in range(1, N + 1):
        for col in range(1, N + 1):
            exactlyOne( clauses, 
                        [generateVar(row, col, val, N) for val in range(1, N + 1)])

    # Exactly 1 val for each value on each row
    # (Xr1v v Xr2v v ... v Xr9v) ^ (-Xr1v v -Xr2v) ^...
    for row in range(1, N + 1):
        for val in range(1, N + 1):
            exactlyOne( clauses,
                        [generateVar(row, col, val, N) for col in range(1, N + 1)])

    # Exactly 1 val for each value on each col
    # (X1cv v X2cv v ... v X9cv) ^ (-X1cv v -X2cv) ^...
    for col in range(1, N + 1):
        for val in range(1, N + 1):
            exactlyOne( clauses,
                        [generateVar(row, col, val, N) for row in range(1, N + 1)])

    # Exactly 1 val for each value on every subgrids
    # Per offsetR, offsetC:
    # (X11v v X12v v ... v XsqrtNsqrtNv) ^ (-X11v v X12v) ^ ...
    for offsetR in range(subN):
        for offsetC in range(subN):
            for val in range(1, N + 1):

                subVars = [generateVar(offsetR * subN + subR, offsetC * subN + subC, val, N)
                        for subR in range(1, subN + 1) 
                        for subC in range(1, subN + 1)]
                
                exactlyOne(clauses, subVars)

    # Appending the given numbers
    for row in range(1, N + 1):
        for col in range(1, N + 1):
            givenVal = grid[row - 1][col - 1]

            if givenVal != 0:  # 0 -> empty square
                clauses.append([generateVar(row, col, givenVal, N)])

    totalVar = N ** 3
    return clauses, totalVar

