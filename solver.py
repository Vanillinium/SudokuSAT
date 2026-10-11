import signal
import time
from pysat.solvers import Glucose3

class TimeoutException(Exception): pass

def timeoutHandler(signum, frame): raise TimeoutException()

def solveSudoku(grid, encoderFunc):
    """
    Solve the Sudoku problem using Glucose3 PySAT solver.
    TIMEOUT when the solver exceeds a certain benchmark.

    :param grid: Sudoku grid of size N x N
    :param encoderFunc: Encoder function
    """

    timeoutBenchmark = 300

    N = len(grid)
    maxVar = N ** 3

    encStart = time.perf_counter()
    clauses, totalVar = encoderFunc(grid)
    encTime = time.perf_counter() - encStart

    signal.signal(signal.SIGALRM, timeoutHandler)
    signal.alarm(timeoutBenchmark)

    solver = Glucose3()
    for clause in clauses:
        solver.add_clause(clause)

    solverStart = time.perf_counter()
    isSat = None
    status = "TIMEOUT"
    
    try:
        solveResult = solver.solve()
        signal.alarm(0)

        solverTime = time.perf_counter() - solverStart
        isSat = solveResult

        status = "SAT" if isSat else "UNSAT"

    except TimeoutException:
        solverTime = float(timeoutBenchmark)
        status = "TIMEOUT"
        isSat = None

    stats = {
        "status" : status,
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