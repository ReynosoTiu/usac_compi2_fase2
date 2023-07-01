from ..Entorno.entorno import Entorno
from ..Entorno.simbolo import Simbolo
from ..Abstract.abstract import Abstract

class Declaration(Abstract):
    def __init__(self, fila, columna, identificador, tipo, expresion=None):
        self.fila = fila
        self.columna = columna
        self.identificador = identificador
        self.expresion = expresion
        self.tipo = tipo

    def interpretar(self, arbol,tabla,entorno: Entorno):

        if self.expresion == None:
            symbol = Simbolo(self.tipo, str(
                self.identificador).lower(), None, self.fila)
        else:
            valor = self.expresion.interpretar(arbol,tabla,entorno)
            # verificar que valor no sea un error o nulo (None)
            symbol = Simbolo(self.tipo, str(
                self.identificador).lower(), valor, self.fila)

        declaracion = entorno.newSymbol(symbol)

        if declaracion == None:
            print("No se pudo declarar la variable " + str(self.identificador))
        return 'ok'
