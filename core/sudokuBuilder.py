from functools import partial
from pysat.card import EncType

from core.encoderCustom import eoBinomal, eoBinary#, eoProduct
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

    # 3: {
    #     "id": 3,
    #     "name": "Product",
    #     "func": lambda grid: generateSudokuClauses(grid, eoProduct)
    # },

    4: {
        "id": 4,
        "name": "Commander/Ladder",
        "func": lambda grid: generateSudokuClauses(grid, partial(eoDefault, encType=EncType.ladder))
    }

}

def getAvailableEncoders():
    return list(ENCODER_FACTORY.values())

def getEncoderByID(id):
    if id == -1:
        return list(ENCODER_FACTORY.values())
    if id in ENCODER_FACTORY:
        return [ENCODER_FACTORY[id]]

    print(f"  -> Invalid Encoder ID ({encoder_id}). Selecting ALL encoders.")
    return list(ENCODER_FACTORY.values())