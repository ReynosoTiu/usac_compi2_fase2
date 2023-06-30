from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
from Instrucciones.Funcion import Funcion


class TypeOf(Funcion):
    def __init__(self, nombre, parametros, instrucciones, fila, columna):
        self.nombre = nombre.lower()
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.NULL_
    
    def interpretar(self, tree, table,gen):
        simbolo = table.getTabla(("toTypeOf##Param1"))
        cadena = ""
        if simbolo == None : 
            return Excepcion("Semantico", "No se encontró el parámetro de Typeof", self.fila, self.columna)
        if simbolo.getTipo() == TIPO.NUMBER:
            cadena = "NUMBER"
        elif simbolo.getTipo() == TIPO.STRING:
            cadena = "STRING"
        elif simbolo.getTipo() == TIPO.BOOLEAN:
            cadena = "BOOLEAN"    
        self.tipo = TIPO.STRING
        return str(cadena)