from TS.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion
from Abstract.NodoAST import NodoAST
from TS.Tipo import TIPO


class To_LowerCase(Instruccion):
    def __init__(self, identificador, fila, columna):
        self.identificador = identificador
        self.fila = fila
        self.columna = columna
        self.tipo = None
        self.arreglo = False

    def interpretar(self, tree, table,gen):
        simbolo = table.getTabla(self.identificador)
        if simbolo == None:
            return Excepcion("Semantico", "Variable " + self.identificador + " no encontrada.", self.fila, self.columna)
        
        if simbolo.getArreglo():
            return Excepcion("Semantico", "Error toLowerCase()" + self.identificador +" no se puede en arreglo completo", self.fila, self.columna)
        
        if simbolo.getTipo() == TIPO.NUMBER:
            return Excepcion("Semantico", "Error toLowerCase()" + self.identificador +" No es de tipo cadena", self.fila, self.columna)
        
        self.tipo = TIPO.STRING #Retorno String
        self.arreglo = simbolo.getArreglo()
        return simbolo.getValor().lower()

    def getNodo(self):
        nodo = NodoAST("toLowerCase")
        nodo.agregarHijo(str(self.identificador))
        return nodo
      