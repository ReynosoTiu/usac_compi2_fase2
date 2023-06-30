from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
from Instrucciones.Funcion import Funcion


class ToLower(Funcion):
    def __init__(self, nombre, parametros, instrucciones, fila, columna):
        self.nombre = nombre
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.NULL_
    
    def interpretar(self, tree, table,gen):
        simbolo = table.getTabla("toLowerCase##Param1")
        if simbolo == None : return Excepcion("Semantico", "No se encontró el parámetro de ToLower", self.fila, self.columna)

        if simbolo.getTipo() != TIPO.STRING:
            return Excepcion("Semantico", "Tipo de parametro de toLower no es cadena.", self.fila, self.columna)

        self.tipo = simbolo.getTipo()
        return simbolo.getValor().lower()