from ..Abstract.abstract import  Abstract
from ..Tabla_Simbolos.Exception import Exception
from ..Abstract.Tipo import TIPO
from ..Tabla_Simbolos.generador import Generador
from ..Abstract.auxiliar import Auxiliar

class Relacionales(Abstract):
    def __init__(self, Op_izq, Op_der, Operador, fila, columna):
        self.Op_izq = Op_izq
        self.Op_der = Op_der
        self.Operador = Operador
        self.tipo = None
        super().__init__(fila, columna)

    def interpretar(self, tree, table):
        genAux = Generador()
        generador = genAux.getInstance()
        generador.addComment("Compilando operacion relacional")

        izq = self.Op_izq.interpretar(tree, table)
        if isinstance(izq, Exception): return izq
        der = None
        result = Auxiliar(None, TIPO.BOOLEAN, False)

        if izq.getTipo() != TIPO.BOOLEAN:
            der = self.Op_der.interpretar(tree, table)
            if isinstance(der, Exception): return der
            if (izq.getTipo() == TIPO.NUMBER) and (der.getTipo() == TIPO.NUMBER):
                self.checkLabels()
                if len(self.Operador) == 3 : self.Operador = self.Operador[:-1]
                generador.addIf(izq.getValue(), der.getValue(), self.Operador, self.getTrueLbl())
                generador.addGoto(self.getFalseLbl())
            elif (izq.getTipo() == TIPO.STRING) and (der.getTipo() == TIPO.STRING):
                if self.Operador == '===' or self.Operador == '!==':
                    generador.fcompareString()
                    paramTemp = generador.addTemp()

                    generador.addExp(paramTemp, 'P', table.size, '+')
                    generador.addExp(paramTemp, paramTemp, '1', '+')
                    generador.setStack(paramTemp, izq.getValue())

                    generador.addExp(paramTemp, paramTemp, '1', '+')
                    generador.setStack(paramTemp, der.getValue())

                    generador.newEnv(table.size)
                    generador.callFun('compareString')

                    temp = generador.addTemp()
                    generador.getStack(temp, 'P')
                    generador.retEnv(table.size)

                    self.checkLabels()
                    generador.addIf(temp, self.getNum(), "==", self.trueLbl)
                    generador.addGoto(self.falseLbl)

                    result.setTrueLbl(self.trueLbl)
                    result.setFalseLbl(self.falseLbl)
                    self.tipo = TIPO.BOOLEAN
                    return result
        elif izq.getTipo() == TIPO.BOOLEAN:
            der = self.Op_der.interpretar(tree, table)
            if isinstance(der, Exception): return der
            if (izq.getTipo() == TIPO.NUMBER) and (der.getTipo() == TIPO.NUMBER):
                self.checkLabels()
                if len(self.Operador) == 3 : self.Operador = self.Operador[:-1]
                generador.addIf(izq.getValue(), der.getValue(), self.Operador, self.getTrueLbl())
                generador.addGoto(self.getFalseLbl())
            elif (izq.getTipo() == TIPO.STRING) and (der.getTipo() == TIPO.STRING):
                if self.Operador == '===' or self.Operador == '!==':
                    generador.fcompareString()
                    paramTemp = generador.addTemp()

                    generador.addExp(paramTemp, 'P', table.size, '+')
                    generador.addExp(paramTemp, paramTemp, '1', '+')
                    generador.setStack(paramTemp, izq.getValue())

                    generador.addExp(paramTemp, paramTemp, '1', '+')
                    generador.setStack(paramTemp, der.getValue())

                    generador.newEnv(table.size)
                    generador.callFun('compareString')

                    temp = generador.addTemp()
                    generador.getStack(temp, 'P')
                    generador.retEnv(table.size)

                    self.checkLabels()
                    generador.addIf(temp, self.getNum(), "==", self.trueLbl)
                    generador.addGoto(self.falseLbl)

                    result.setTrueLbl(self.trueLbl)
                    result.setFalseLbl(self.falseLbl)
                    self.tipo = TIPO.BOOLEAN
                    return result

            # generador.addComment("ERROR: No se admiten boolean para operaciones relacionales")
            # # seteamos los label para evitar el error al compilar en golang, "etiquetas no definidas"
            # generador.putLabel(izq.trueLbl)
            # generador.putLabel(izq.falseLbl)
            # return Error("Semantico", "No se admiten boolean para operaciones relacionales", self.fila, self.columna)
        generador.addComment("Fin de compilacion de Expresion Relacional")
        generador.addSpace()

        result.setTrueLbl(self.trueLbl)
        result.setFalseLbl(self.falseLbl)
        self.tipo = TIPO.BOOLEAN
        return result
    def checkLabels(self):
        genAux = Generador()
        generador = genAux.getInstance()
        if self.trueLbl == '':
            self.trueLbl = generador.newLabel()
        if self.falseLbl == '':
            self.falseLbl = generador.newLabel()

    def getTipo(self):
        return self.tipo

    def getNum(self):
        if self.Operador == '===':
            return '1'
        if self.Operador == '!==':
            return '0'