import time
from pysat.solvers import Glucose3

def solveSudoku(grid, encoderFunc):
    N = len(grid)
    maxVar = N ** 3

    encStart = time.perf_counter()
    clauses, totalVar = encoderFunc(grid)
    encTime = time.perf_counter() - encStart

    solver = Glucose3()
    for clause in clauses:
        solver.add_clause(clause)

    solverStart = time.perf_counter()
    solver.conf_budget(1000000)
    isSat = solver.solve_limited()
    solverTime = time.perf_counter() - solverStart

    stats = {
        "isSat": isSat,
        "gridSize": f"{N}x{N}",
        "maxVar": maxVar,
        "totalVar": totalVar,
        "auxVar": totalVar - maxVar,
        "numClauses": len(clauses),
        "encTime": encTime,
        "solverTime": solverTime,
        "totalTime": encTime + solverTime
    }

    solver.delete()
    return stats