from functools import partial
from pysat.card import EncType

from core.encoderCustom import eoBinomal, eoBinary, eoProduct
from core.encoderPySATDefault import eoDefault

from core.generateSudokuClauses import generateSudokuClauses

ENCODER_FACTORY = {
    0: {
        "id": 0,
        "name": "Binomal/Pairwise",
        "func": lambda grid: generateSudokuClauses(grid, eoBinomal)
    },

    1: {
        "id": 1,
        "name": "Binary/Bitwise",
        "func": lambda grid: generateSudokuClauses(grid, eoBinary)
    },

    2: {
        "id": 2,
        "name": "Sequential",
        "func": lambda grid: generateSudokuClauses(grid, partial(eoDefault, encType=EncType.seqcounter))
    },

    3: {
        "id": 3,
        "name": "Product",
        "func": lambda grid: generateSudokuClauses(grid, eoProduct)
    },

    4: {
        "id": 4,
        "name": "Commander/Ladder",
        "func": lambda grid: generateSudokuClauses(grid, partial(eoDefault, encType=EncType.ladder))
    }

}

def getAvailableEncoders():
    return list(ENCODER_FACTORY.values())

def getEncoderByID(ids):
    if not ids or -1 in ids:
        return list(ENCODER_FACTORY.values())

    if isinstance(ids, int):
        ids = [ids]

    selected = []
    for id in ids:
        if id in ENCODER_FACTORY:
            selected.append(ENCODER_FACTORY[id])
        else:
            print(f" -> Warning: ID {id} is invalid. Skipped.")  
    
    if not selected:
        print(" -> No valid encoders selected. Selecting ALL encoders.")
        return list(ENCODER_FACTORY.values())

    return selected