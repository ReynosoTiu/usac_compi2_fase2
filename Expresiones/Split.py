from TS.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion
from Abstract.NodoAST import NodoAST
from TS.Tipo import TIPO


class Split(Instruccion):
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
        
        if simbolo.getTipo() == TIPO.NUMBER:
            return Excepcion("Semantico", "Error en split " + self.identificador +" debe ser una cadena", self.fila, self.columna)
        
        self.tipo = TIPO.STRING #Retorno String
        self.arreglo = True
        valor = self.expresion.interpretar(tree,table)
        
        if isinstance(valor, Excepcion):
            return valor
        
        return simbolo.getValor().split(valor)

    def getNodo(self):
        nodo = NodoAST("split")
        nodo.agregarHijo(str(self.identificador))
        return nodo
      