from Abstract.Instruccion import Instruccion
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO, OperadorRelacional
from Abstract.Value import Value

class Relacional(Instruccion):
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
        if isinstance(izq, Excepcion): 
            return izq
        der = self.OperacionDer.interpretar(tree, table,gen)
        if isinstance(der, Excepcion): 
            return der
        
        if self.operador == OperadorRelacional.MENOR:
            #_______________________________ < ___________________
            if self.OperacionIzq.tipo == TIPO.NUMBER and self.OperacionDer.tipo == TIPO.NUMBER:
                trueLabel = gen.newLabel()
                falseLabel = gen.newLabel()

                gen.AddIf(izq.valor,der.valor, "<", trueLabel)
                gen.AddGoto(falseLabel)
                val = Value("",False,self.tipo)
                val.TrueLvl.append(trueLabel)
                val.FalseLvl.append(falseLabel)

                return val
            
            elif self.OperacionIzq.tipo == TIPO.STRING and self.OperacionDer.tipo == TIPO.STRING:
                #Hay error aqui en golang no se puede comparar string
                trueLabel = gen.newLabel()
                falseLabel = gen.newLabel()

                gen.AddIf(izq.valor,der.valor, "<", trueLabel)
                gen.AddGoto(falseLabel)
                val = Value("",False,self.tipo)
                val.TrueLvl.append(trueLabel)
                val.FalseLvl.append(falseLabel)

                return val
                #return self.obtenerVal(self.OperacionIzq.tipo, izq) < self.obtenerVal(self.OperacionDer.tipo, der)
            return Excepcion("Semantico", "Tipo Erroneo de operacion para <.", self.fila, self.columna)

        elif self.operador == OperadorRelacional.MENORIGUAL:
            #____________________________ <= ___________________________
            if self.OperacionIzq.tipo == TIPO.NUMBER and self.OperacionDer.tipo == TIPO.NUMBER:
                trueLabel = gen.newLabel()
                falseLabel = gen.newLabel()

                gen.AddIf(izq.valor,der.valor, "<=", trueLabel)
                gen.AddGoto(falseLabel)
                val = Value("",False,self.tipo)
                val.TrueLvl.append(trueLabel)
                val.FalseLvl.append(falseLabel)

                return val
            elif self.OperacionIzq.tipo == TIPO.STRING and self.OperacionDer.tipo == TIPO.STRING:
                #Error aqui
                trueLabel = gen.newLabel()
                falseLabel = gen.newLabel()

                gen.AddIf(izq.valor,der.valor, "<=", trueLabel)
                gen.AddGoto(falseLabel)
                val = Value("",False,self.tipo)
                val.TrueLvl.append(trueLabel)
                val.FalseLvl.append(falseLabel)

                return val
            return Excepcion("Semantico", "Tipo Erroneo de operacion para <=.", self.fila, self.columna)

        elif self.operador == OperadorRelacional.MAYOR:
            #____________________________ > ___________________________
            if self.OperacionIzq.tipo == TIPO.NUMBER and self.OperacionDer.tipo == TIPO.NUMBER:
                trueLabel = gen.newLabel()
                falseLabel = gen.newLabel()

                gen.AddIf(izq.valor,der.valor, ">", trueLabel)
                gen.AddGoto(falseLabel)
                val = Value("",False,self.tipo)
                val.TrueLvl.append(trueLabel)
                val.FalseLvl.append(falseLabel)

                return val
            elif self.OperacionIzq.tipo == TIPO.STRING and self.OperacionDer.tipo == TIPO.STRING:
                #Error Aqui verificar
                trueLabel = gen.newLabel()
                falseLabel = gen.newLabel()

                gen.AddIf(izq.valor,der.valor, ">", trueLabel)
                gen.AddGoto(falseLabel)
                val = Value("",False,self.tipo)
                val.TrueLvl.append(trueLabel)
                val.FalseLvl.append(falseLabel)

                return val
            return Excepcion("Semantico", "Tipo Erroneo de operacion para >.", self.fila, self.columna)

        elif self.operador == OperadorRelacional.MAYORIGUAL:
            #____________________________ >= ___________________________
            if self.OperacionIzq.tipo == TIPO.NUMBER and self.OperacionDer.tipo == TIPO.NUMBER:
                trueLabel = gen.newLabel()
                falseLabel = gen.newLabel()

                gen.AddIf(izq.valor,der.valor, ">=", trueLabel)
                gen.AddGoto(falseLabel)
                val = Value("",False,self.tipo)
                val.TrueLvl.append(trueLabel)
                val.FalseLvl.append(falseLabel)

                return val

            elif self.OperacionIzq.tipo == TIPO.STRING and self.OperacionDer.tipo == TIPO.STRING:
                #Error EN comparar string
                trueLabel = gen.newLabel()
                falseLabel = gen.newLabel()

                gen.AddIf(izq.valor,der.valor, ">=", trueLabel)
                gen.AddGoto(falseLabel)
                val = Value("",False,self.tipo)
                val.TrueLvl.append(trueLabel)
                val.FalseLvl.append(falseLabel)

                return val
            return Excepcion("Semantico", "Tipo Erroneo de operacion para >=.", self.fila, self.columna)


        elif self.operador == OperadorRelacional.IGUALIGUAL:
            #_________________________________ == _________________________________

            if self.OperacionIzq.tipo == TIPO.NUMBER and self.OperacionDer.tipo == TIPO.NUMBER:
                trueLabel = gen.newLabel()
                falseLabel = gen.newLabel()

                gen.AddIf(izq.valor,der.valor, "==", trueLabel)
                gen.AddGoto(falseLabel)
                val = Value("",False,self.tipo)
                val.TrueLvl.append(trueLabel)
                val.FalseLvl.append(falseLabel)

                return val
            elif self.OperacionIzq.tipo == TIPO.STRING and self.OperacionDer.tipo == TIPO.STRING:
                #Error Verificar aqui xD
                trueLabel = gen.newLabel()
                falseLabel = gen.newLabel()

                gen.AddIf(izq.valor,der.valor, "==", trueLabel)
                gen.AddGoto(falseLabel)
                val = Value("",False,self.tipo)
                val.TrueLvl.append(trueLabel)
                val.FalseLvl.append(falseLabel)

                return val
            return Excepcion("Semantico", "Tipo Erroneo de operacion para ==.", self.fila, self.columna)
        elif self.operador == OperadorRelacional.DISTINTO:
            #_________________________________ != _________________________________

            if self.OperacionIzq.tipo == TIPO.NUMBER and self.OperacionDer.tipo == TIPO.NUMBER:
                trueLabel = gen.newLabel()
                falseLabel = gen.newLabel()

                gen.AddIf(izq.valor,der.valor, "!=", trueLabel)
                gen.AddGoto(falseLabel)
                val = Value("",False,self.tipo)
                val.TrueLvl.append(trueLabel)
                val.FalseLvl.append(falseLabel)

                return val
            elif self.OperacionIzq.tipo == TIPO.STRING and self.OperacionDer.tipo == TIPO.STRING:
                trueLabel = gen.newLabel()
                falseLabel = gen.newLabel()

                gen.AddIf(izq.valor,der.valor, "!=", trueLabel)
                gen.AddGoto(falseLabel)
                val = Value("",False,self.tipo)
                val.TrueLvl.append(trueLabel)
                val.FalseLvl.append(falseLabel)

                return val
            return Excepcion("Semantico", "Tipo Erroneo de operacion para =!.", self.fila, self.columna)
        return Excepcion("Semantico", "Tipo de Operacion no Especificado.", self.fila, self.columna)

    def obtenerVal(self, tipo, val):
        if tipo == TIPO.NUMBER:
            return float(val)
        elif tipo == TIPO.BOOLEAN:
            return bool(val)
        return str(val)
    
    def getNodo(self):
        nodo = NodoAST("RELACIONAL")
        nodo.agregarHijoNodo(self.OperacionIzq.getNodo())
        nodo.agregarHijo(str(self.operador))
        nodo.agregarHijoNodo(self.OperacionDer.getNodo())
        return nodo
        