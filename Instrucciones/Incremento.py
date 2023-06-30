from TS.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion
from Abstract.NodoAST import NodoAST
from TS.Simbolo import Simbolo
from TS.Tipo import OperadorIncremento
from TS.Tipo import TIPO
from Abstract.Value import Value


class Incremento(Instruccion):
    def __init__(self, identificador,tipo_aumento, fila, columna):
        self.identificador = identificador.lower()
        self.tipo_aumento = tipo_aumento
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table,gen):
        temp_simbolo = table.getTabla(self.identificador)
        
        if self.tipo_aumento == OperadorIncremento.MASMAS:
            if temp_simbolo.tipo == TIPO.NUMBER:
                gen.AddComment("====================    GENERANDO EXPRESION++   ===================")
                newTemp = gen.newTemp()
                newTempAsignacion = gen.newTemp()
                gen.AddGetStack(newTemp,"int("+str(temp_simbolo.posicion)+")")
                gen.AddAssign(newTempAsignacion,newTemp+"+ 1")
                gen.AddSetStack("int("+str(temp_simbolo.posicion)+")",newTempAsignacion)
                return None
            return Excepcion("Semantico","Error El incremento debe ser un number",self.fila,self.columna)
        elif  self.tipo_aumento == OperadorIncremento.MENOSMENOS:
            if temp_simbolo.tipo == TIPO.NUMBER:
                gen.AddComment("====================    GENERANDO EXPRESION++   ===================")
                newTemp = gen.newTemp()
                newTempAsignacion = gen.newTemp()
                gen.AddGetStack(newTemp,"int("+str(temp_simbolo.posicion)+")")
                gen.AddAssign(newTempAsignacion,newTemp+"- 1")
                gen.AddSetStack("int("+str(temp_simbolo.posicion)+")",newTempAsignacion)
                return None
            return Excepcion("Semantico","Error El incremento debe ser un number",self.fila,self.columna)
        return Excepcion("Semantico","Error Tipo de operador de incremento no existe en for",self.fila,self.columna)
    
    def getNodo(self):
        nodo = NodoAST("INCREMENTO")
        nodo.agregarHijo(str(self.identificador))
        nodo.agregarHijo(str(self.tipo_aumento))

        #nodo.agregarHijoNodo(self.expresion.getNodo())
        return nodo