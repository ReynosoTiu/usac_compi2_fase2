from enum import Enum

class TIPO(Enum):
    NUMBER = 1
    BOOLEAN = 2
    STRING = 3
    NULL_ = 4
    ARREGLO = 7
    ANY = 8
    VOID = 9

class OperadorAritmetico(Enum):
    MAS = 1
    MENOS = 2
    POR = 3
    DIV = 4
    POT = 5
    MOD = 6
    UMENOS = 7

class OperadorRelacional(Enum):
    MENOR = 1
    MAYOR = 2
    MENORIGUAL = 3
    MAYORIGUAL = 4
    IGUALIGUAL = 5
    DISTINTO = 6

class OperadorLogico(Enum):
    NOT = 1
    AND = 2
    OR = 3
class OperadorIncremento(Enum):
    MASMAS = 1
    MENOSMENOS = 2