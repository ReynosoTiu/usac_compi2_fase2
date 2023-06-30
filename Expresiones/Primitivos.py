from Abstract.Instruccion import Instruccion
from Abstract.Value import Value
from Abstract.NodoAST import NodoAST
from TS.Tipo import TIPO

class Primitivos(Instruccion):
    def __init__(self, tipo, valor, fila, columna):
        self.tipo = tipo
        self.valor = valor
        self.fila = fila
        self.columna = columna
        self.arreglo = False

    def interpretar(self, tree, table,gen):
        if self.tipo == TIPO.NUMBER:
            gen.AddComment("====================    PRIMITIVO NUMBER  ====================")
            gen.AddBr()
            return Value(str(float(self.valor)),False,self.tipo)
        elif self.tipo == TIPO.STRING:
            gen.AddComment("====================    PRIMITIVO STRING  ====================")
            #nuevo temporal
            newTemp = gen.newTemp()
            #igualar a Heap Pointer
            gen.AddAssign(newTemp, "H")
            #recorrer cadena
            for char in str(self.valor):
                #se agrega ascii a heap
                gen.AddSetHeap("int(H)", str(ord(char)))
                #suma heap pointer
                gen.AddExpression("H", "H", "1", "+")
            #caracteres de escape
            gen.AddSetHeap("int(H)", "-1")
            gen.AddExpression("H", "H", "1", "+")
            gen.AddBr()
            return Value(newTemp,True,self.tipo)
        elif self.tipo == TIPO.BOOLEAN:
            gen.AddComment("====================    PRIMITIVO BOOL  ====================")
            trueLabel = gen.newLabel()
            falseLabel = gen.newLabel()
            if bool(self.valor):
                gen.AddGoto(trueLabel)
                gen.AddGoto(falseLabel)
            else:
                gen.AddGoto(falseLabel)
                gen.AddGoto(trueLabel)
            val = Value("",False,self.tipo)
            val.TrueLvl.append(trueLabel)
            val.FalseLvl.append(falseLabel)
            gen.AddBr()
            return val
        
        return Exception("Semantico",str(self.tipo) + "no existe...",self.fila,self.columna)
    
    def getNodo(self):
        nodo = NodoAST("PRIMITIVO")
        nodo.agregarHijo(str(self.valor))
        return nodo
