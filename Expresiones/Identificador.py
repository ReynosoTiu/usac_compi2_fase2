from TS.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion
from Abstract.NodoAST import NodoAST
from Abstract.Value import Value
from TS.Tipo import TIPO


class Identificador(Instruccion):
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
        self.tipo = simbolo.getTipo()
        self.arreglo = simbolo.getArreglo()
        
        newTemp = gen.newTemp()
        if simbolo.tipo == TIPO.NUMBER:
            gen.AddComment("==================== ACCESP NUMBER ====================")
            gen.AddGetStack(newTemp,"int("+str(simbolo.posicion)+")")
            return Value(newTemp,True,simbolo.tipo)
        
        if simbolo.tipo == TIPO.STRING:
            gen.AddComment("==================== ACCESO STRING ====================")
            gen.AddGetStack(newTemp,"int("+str(simbolo.posicion)+")")
            return Value(newTemp,True,simbolo.tipo)
        
        if simbolo.tipo == TIPO.BOOLEAN:
            gen.AddComment("==================== ACCESO BOLEAN ====================")
            gen.AddGetStack(newTemp,"int("+str(simbolo.posicion)+")")
            val = Value(newTemp,True,simbolo.tipo)
            
            trueLabel = gen.newLabel()
            falseLabel = gen.newLabel()
            val.TrueLvl.append(trueLabel)
            val.FalseLvl.append(falseLabel)
            return val

        return Excepcion("Semantico", "Error tipo " + str(simbolo.tipo) + " no encontrada.", self.fila, self.columna)

    def getNodo(self):
        nodo = NodoAST("IDENTIFICADOR")
        nodo.agregarHijo(str(self.identificador))
        return nodo
        
    
        