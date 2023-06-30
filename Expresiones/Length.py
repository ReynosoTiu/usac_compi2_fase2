from TS.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion
from Abstract.NodoAST import NodoAST
from TS.Tipo import TIPO


class Length(Instruccion):
    def __init__(self, identificador, fila, columna):
        self.identificador = identificador
        self.fila = fila
        self.columna = columna
        self.tipo = None
        self.arreglo = False

    def interpretar(self, tree, table,gen):
        simbolo = table.getTabla(self.identificador)
        if simbolo == None :
            return Excepcion("Semantico", "", self.fila, self.columna)
        
        if simbolo.getArreglo() == True:
            self.tipo = TIPO.NUMBER
            return len(simbolo.getValor())

        if simbolo.getTipo() == TIPO.STRING and simbolo.getArreglo() == False :
            self.tipo = TIPO.NUMBER
            return len(simbolo.getValor())
        return Excepcion("Semantico", "Tipo de parametro de Length  no es cadena o arreglo.", self.fila, self.columna)

    def getNodo(self):
        nodo = NodoAST("Length")
        nodo.agregarHijo(str(self.identificador))
        return nodo
      