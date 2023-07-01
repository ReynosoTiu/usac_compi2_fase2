from enum import Enum

class TIPO(Enum):
    NUMBER = 1
    STRING = 2
    BOOLEAN = 3
    ANY = 4
    NULL = 5

class NATIVA(Enum):
    APROXIMACION = 1
    EXPONENCIAL = 2
    STRING = 3
    LOWER = 4
    UPPER = 5
    SPLIT = 6
    CONCATENACION = 7
    TYPEOF = 8
    ARRAY = 10