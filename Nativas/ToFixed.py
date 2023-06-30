from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
from Instrucciones.Funcion import Funcion


class ToFixed(Funcion):
    def __init__(self, nombre, parametros, instrucciones, fila, columna):
        self.nombre = nombre
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.NULL_
    
    def interpretar(self, tree, table,gen):
        simbolo = table.getTabla(("toFixed##Param1"))
        if simbolo == None : return Excepcion("Semantico", "No se encontró el parámetro de toFixed", self.fila, self.columna)
        
        if simbolo.getArreglo() == True:
            return Excepcion("Semantico", "Error simbolo de tipo arreglo", self.fila, self.columna)

        if simbolo.getTipo() == TIPO.NUMBER and simbolo.getArreglo() == False :
            self.tipo = TIPO.NUMBER
            return round(simbolo.getValor())
        
        return Excepcion("Semantico", "Error Tipo de parametro de toFixed  no es number", self.fila, self.columna)