from pysat.card import CardEnc

def eoDefault(clauses, vars, currTopVar, encType):
    """
    Default frame to build the library's default encoders.
    
    :param clauses: List of already-appended CNF clauses
    :param vars: List of literal variables
    :param currTopVar: Largest ID of the variables
    :param encType: PySAT's encoder type

    :return: currTopVar after appending more auxilary variables.
    """
    cnf = CardEnc.equals(lits=vars, bound=1, top_id=currTopVar, encoding=encType)
    newTopVar = max(cnf.nv, currTopVar)

    clauses.extend(cnf.clauses)

    return newTopVar
