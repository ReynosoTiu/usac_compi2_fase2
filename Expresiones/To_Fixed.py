from TS.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion
from Abstract.NodoAST import NodoAST
from TS.Tipo import TIPO


class To_Fixed(Instruccion):
    def __init__(self, identificador,expresion, fila, columna):
        self.identificador = identificador
        self.expresion = expresion
        self.fila = fila
        self.columna = columna
        self.tipo = None
        self.arreglo = False

    def interpretar(self, tree, table,gen):
        simbolo = table.getTabla(self.identificador)
        if simbolo == None:
            return Excepcion("Semantico", "Variable " + self.identificador + " no encontrada.", self.fila, self.columna)
        
        print("Antes de tofixed")
        if simbolo.getTipo() == TIPO.STRING:
            return Excepcion("Semantico", "Error en funciona ToFixed" + self.identificador +"es de "+str(simbolo.getTipo()), self.fila, self.columna)
        print("despues de tofixed")
        self.tipo = simbolo.getTipo()
        self.arreglo = simbolo.getArreglo()
        decimales = self.expresion.interpretar(tree,table)
        
        if isinstance(decimales, Excepcion):
            return decimales
        print("Aqui paso en toFixen")
        return round(simbolo.getValor(),decimales)

    def getNodo(self):
        nodo = NodoAST("toFixed")
        nodo.agregarHijo(str(self.identificador))
        return nodo
      