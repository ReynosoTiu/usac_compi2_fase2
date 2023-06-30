from Abstract.Instruccion import Instruccion
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO, OperadorAritmetico
from Abstract.Value import Value

class Aritmetica(Instruccion):
    def __init__(self, operador, OperacionIzq, OperacionDer, fila, columna):
        self.operador = operador
        self.OperacionIzq = OperacionIzq
        self.OperacionDer = OperacionDer
        self.fila = fila
        self.columna = columna
        self.tipo = None
        self.arreglo = False

    
    def interpretar(self, tree, table,gen):
        izq = self.OperacionIzq.interpretar(tree, table,gen)
        if isinstance(izq, Excepcion): return izq
        if self.OperacionDer != None:
            der = self.OperacionDer.interpretar(tree, table,gen)
            if isinstance(der, Excepcion): return der

        newTemp = gen.newTemp()
        if self.operador == OperadorAritmetico.MAS: #SUMA
            gen.AddComment("==================== OPERACION SUMA ====================")
            #------------------NUMBER VRS TIPOS------------------------------------
            if self.OperacionIzq.tipo == TIPO.NUMBER and self.OperacionDer.tipo == TIPO.NUMBER:
                #number + number
                self.tipo = TIPO.NUMBER
                gen.AddExpression(newTemp,izq.valor,der.valor,"+")
                return Value(newTemp,True,self.tipo)
            elif self.OperacionIzq.tipo == TIPO.NUMBER and self.OperacionDer.tipo == TIPO.STRING:
                #number + string
                #Aqui esta mal Revisar xD opeacion con suma y string no hay validadcion xD
                self.tipo = TIPO.STRING
                gen.AddExpression(newTemp,izq.valor,der.valor,"+")
                return Value(newTemp,True,self.tipo)
            #------------------------ string vrs tipos ---------------------------------------
            if self.OperacionIzq.tipo == TIPO.STRING and self.OperacionDer.tipo == TIPO.NUMBER:
                #string + number
                self.tipo = TIPO.STRING
                gen.AddExpression(newTemp,izq.valor,der.valor,"+")
                return Value(newTemp,True,self.tipo)
            elif self.OperacionIzq.tipo == TIPO.STRING and self.OperacionDer.tipo == TIPO.STRING:
                #string + string
                self.tipo = TIPO.STRING
                gen.AddExpression(newTemp,izq.valor,der.valor,"+")
                return Value(newTemp,True,self.tipo)
            return Excepcion("Semantico", "Tipo Erroneo de operacion para +.", self.fila, self.columna)

        elif self.operador == OperadorAritmetico.MENOS: #RESTA
            #------------------------------ number vrs tipos ----------------------------------
            if self.OperacionIzq.tipo == TIPO.NUMBER and self.OperacionDer.tipo == TIPO.NUMBER:
                # number  - number
                self.tipo = TIPO.NUMBER
                gen.AddExpression(newTemp,izq.valor,der.valor,"-")
                return Value(newTemp,True,self.tipo)
            return Excepcion("Semantico", "Tipo Erroneo de operacion para -.", self.fila, self.columna)
        
        elif self.operador == OperadorAritmetico.POR: #Multiplicacion
            #--------------------------- number vrs tipos ------------------------------------
            if self.OperacionIzq.tipo == TIPO.NUMBER and self.OperacionDer.tipo == TIPO.NUMBER:
                #number * number
                self.tipo = TIPO.NUMBER
                gen.AddExpression(newTemp,izq.valor,der.valor,"*")
                return Value(newTemp,True,self.tipo)
            return Excepcion("Semantico", "Tipo Erroneo de operacion para *.", self.fila, self.columna)

        elif self.operador == OperadorAritmetico.DIV: #Division
            #--------------------------- number vrs tipos ------------------------------------
            if self.OperacionIzq.tipo == TIPO.NUMBER and self.OperacionDer.tipo == TIPO.NUMBER:
                #number / number
                self.tipo = TIPO.NUMBER
                gen.AddExpression(newTemp,izq.valor,der.valor,"/")
                return Value(newTemp,True,self.tipo)
            return Excepcion("Semantico", "Tipo Erroneo de operacion para /.", self.fila, self.columna)
        
        elif self.operador == OperadorAritmetico.POT: #POTENCIA
            #--------------------------- number vrs tipos ------------------------------------
            if self.OperacionIzq.tipo == TIPO.NUMBER and self.OperacionDer.tipo == TIPO.NUMBER:
                #number ^ number
                #Analizar potencia en golang necesita libreria
                self.tipo = TIPO.NUMBER
                gen.AddExpressionPOT(newTemp,izq.valor,der.valor)
                return Value(newTemp,True,self.tipo)
            return Excepcion("Semantico", "Tipo Erroneo de operacion para **.", self.fila, self.columna)
        
        elif self.operador == OperadorAritmetico.MOD: #MODULO
            #--------------------------- number vrs tipos ------------------------------------
            if self.OperacionIzq.tipo == TIPO.NUMBER and self.OperacionDer.tipo == TIPO.NUMBER:
                #number % number
                self.tipo = TIPO.NUMBER
                gen.AddExpressionMOD(newTemp,izq.valor,der.valor,"%")
                return Value(newTemp,True,self.tipo)
            return Excepcion("Semantico", "Tipo Erroneo de operacion para %.", self.fila, self.columna)
        if self.operador == OperadorAritmetico.UMENOS: #NEGACION UNARIA
            if self.OperacionIzq.tipo == TIPO.NUMBER:
                self.tipo = TIPO.NUMBER
                gen.AddExpression(newTemp,"-"+izq.valor,"","")
                return Value(newTemp,True,self.tipo)
                #return - self.obtenerVal(self.OperacionIzq.tipo, izq)
            return Excepcion("Semantico", "Tipo Erroneo de operacion para - unario.", self.fila, self.columna)
        return Excepcion("Semantico", "Tipo de Operacion no Especificado.", self.fila, self.columna)



    def obtenerVal(self, tipo, val):
        if tipo == TIPO.NUMBER:
            return float(val)
        elif tipo == TIPO.BOOLEAN:
            return bool(val)
        return str(val)
    
    def getNodo(self):
        nodo = NodoAST("ARITMETICA")
        if self.OperacionDer != None:
            nodo.agregarHijoNodo(self.OperacionIzq.getNodo())
            nodo.agregarHijo(str(self.operador))
            nodo.agregarHijoNodo(self.OperacionDer.getNodo())
        else:
            nodo.agregarHijo(str(self.operador))
            nodo.agregarHijoNodo(self.OperacionIzq.getNodo())
        
        return nodo
        