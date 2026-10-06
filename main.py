from solver import solveSudoku
from core.generateSudokuProblem import generate_random_sudoku as gen
from core.sudokuBuilder import getAvailableEncoders, getEncoderByID

GRID_SAMPLES = {9, 16, 25, 36}

def simulation(encoderFunc, encoderName, gridSize, iterations):
    print(f"\n[+] Running simulation {iterations} times | Encoder: {encoderName}")

    totalEncTime = 0.0
    totalSolverTime = 0.0
    sampleStats = None
    
    totalRuns = iterations

    while iterations > 0:
        iterations -= 1

        currGrid = gen(gridSize)

        stats = solveSudoku(currGrid, encoderFunc)
        if not stats or not stats.get("isSat", False):
            return None

        totalEncTime += stats["encTime"]
        totalSolverTime += stats["solverTime"]
        sampleStats = stats

    avgStats = {
        "encoder": encoderName,
        "gridSize": sampleStats["gridSize"],
        "totalVar": sampleStats["totalVar"],
        "auxVar": sampleStats["auxVar"],
        "numClauses": sampleStats["numClauses"],
        "avgEncodingTime": totalEncTime / totalRuns,
        "avgSolvingTime": totalSolverTime / totalRuns,
        "avgTotalTime": (totalEncTime + totalSolverTime) / totalRuns
    }

    return avgStats


if __name__ == "__main__":
    # ---INPUTS---

    # GRID SIZE
    try:
        gridSize = int(input("\n[?] Input grid size (9, 16, 25, 36): "))
    except ValueError:
        gridSize = 9
        print("  -> Invalid input, defaulting to 9.")

    if gridSize not in GRID_SAMPLES:
        print(f"  -> Invalid input, defaulting to 9.")
        gridSize = 9

    # ENCODER
    encoders = getAvailableEncoders()
    print("\nList of available encoders:")

    for enc in encoders:
        print(f"   [{enc['id']}] {enc['name']}")
        
    print("   [-1] ALL (default)")

    try:
        choice = int(input("\n[?] Input encoder (-1 to select all): "))
    except ValueError:
        choice = -1

    encSelected = getEncoderByID(choice)

    # SIM AMOUNT
    try:
        numSimulation = int(input("\n[?] Input simulation amount: "))
    except ValueError:
        print("  -> Invalid amount, defaulting to 100 tries.")
        numSimulation = 100


    # ---RUNNING SIM---
    print("\n" + "="*40)
    print("         RUNNING SIMULATION          ")
    print("="*40)

    results = []
    for enc in encSelected:
        res = simulation(
            encoderFunc=enc["func"],
            encoderName=enc["name"],
            gridSize=gridSize,
            iterations=numSimulation
        )
        if res:
            results.append(res)

    # --- RESULT---
    print("\n" + "="*50)
    print("               RESULTS                      ")
    print("="*50)
    print(f" Grid Size            : {res['gridSize']}")
    for res in results:
        print(f" - Encoder            : {res['encoder']}")
        print(f"   + Variable amount  : {res['totalVar']} (Aux: {res['auxVar']})")
        print(f"   + Clause amount    : {res['numClauses']}")
        print(f"   + Avg encoding time: {res['avgEncodingTime'] * 1000:.4f} ms")
        print(f"   + Avg solving time : {res['avgSolvingTime'] * 1000:.4f} ms")
        print(f"   + Avg total time   : {res['avgTotalTime'] * 1000:.4f} ms")
        print("-" * 50)