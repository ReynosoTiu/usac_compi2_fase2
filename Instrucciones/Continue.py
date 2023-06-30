from Abstract.Instruccion import Instruccion
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
from TS.TablaSimbolos import TablaSimbolos

class Continue(Instruccion):
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table,gen):
        return self
    
    def getNodo(self):
        nodo = NodoAST("CONTINUE")
        return nodo