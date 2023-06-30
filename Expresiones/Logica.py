from Abstract.Instruccion import Instruccion
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO, OperadorLogico
from Abstract.Value import Value
class Logica(Instruccion):
    def __init__(self, operador, OperacionIzq, OperacionDer, fila, columna):
        self.operador = operador
        self.OperacionIzq = OperacionIzq
        self.OperacionDer = OperacionDer
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.BOOLEAN
        self.arreglo = False

    
    def interpretar(self, tree, table,gen):
        
        izq = self.OperacionIzq.interpretar(tree, table,gen)
        if isinstance(izq, Excepcion): return izq
        if self.OperacionDer != None:
            der = self.OperacionDer.interpretar(tree, table,gen)
            if isinstance(der, Excepcion): return der

        if self.operador == OperadorLogico.AND:
            if self.OperacionIzq.tipo == TIPO.BOOLEAN and self.OperacionDer.tipo == TIPO.BOOLEAN:
                #se agregan etiquetas verdaderas de op1
                for i in  range(len(izq.TrueLvl)):
                    gen.AddLabel(izq.TrueLvl[i])
                
                val = Value("", False,self.tipo)

                val.TrueLvl += der.TrueLvl
                val.FalseLvl += izq.FalseLvl
                val.FalseLvl += der.FalseLvl

                return val
            return Excepcion("Semantico", "Tipo Erroneo de operacion para &&.", self.fila, self.columna)
        elif self.operador == OperadorLogico.OR:
            if self.OperacionIzq.tipo == TIPO.BOOLEAN and self.OperacionDer.tipo == TIPO.BOOLEAN:
                #se agregan etiquetas falsas de op1
                for i  in range(len(izq.FalseLvl)):
                    gen.AddLabel(izq.FalseLvl[i])

                val = Value("", False,self.tipo)

                val.TrueLvl += izq.TrueLvl
                val.TrueLvl += der.TrueLvl
                val.FalseLvl += der.FalseLvl
                return val
            return Excepcion("Semantico", "Tipo Erroneo de operacion para ||.", self.fila, self.columna)
        elif self.operador == OperadorLogico.NOT:
            if self.OperacionIzq.tipo == TIPO.BOOLEAN:
                val = Value("",False, self.tipo)
                val.TrueLvl += izq.FalseLvl
                val.FalseLvl += izq.TrueLvl
                return val
                return not self.obtenerVal(self.OperacionIzq.tipo, izq)
            return Excepcion("Semantico", "Tipo Erroneo de operacion para !.", self.fila, self.columna)
        return Excepcion("Semantico", "Tipo de Operacion no Especificado.", self.fila, self.columna)

    def obtenerVal(self, tipo, val):
        if tipo == TIPO.NUMBER:
            return float(val)
        elif tipo == TIPO.BOOLEAN:
            return bool(val)
        return str(val)
    
    def getNodo(self):
        nodo = NodoAST("LOGICA")
        if self.OperacionDer != None:
            nodo.agregarHijoNodo(self.OperacionIzq.getNodo())
            nodo.agregarHijo(str(self.operador))
            nodo.agregarHijoNodo(self.OperacionDer.getNodo())
        else:
            nodo.agregarHijo(str(self.operador))
            nodo.agregarHijoNodo(self.OperacionIzq.getNodo())
        
        return nodo
        