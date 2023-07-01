from ..Abstract.abstract import Abstract
from ..Abstract.Tipo import TIPO
from ..Tabla_Simbolos.Exception import Exception
from ..Tabla_Simbolos.generador import Generador
from ..Abstract.auxiliar import Auxiliar

class Logicas(Abstract):
    def __init__(self, Op_izq, Op_der, Operador, fila, columna):
        self.Op_izq = Op_izq
        self.Op_der = Op_der
        self.Operador = Operador
        self.tipo = TIPO.BOOLEAN
        super().__init__(fila, columna)

    def interpretar(self, tree, table):
        genAux = Generador()
        generador = genAux.getInstance()

        generador.addComment("Compilacion de Expresion Relacional")
        self.checkLabels()
        templa = ''

        if self.Operador == '&&':
            templa = generador.newLabel()
            self.Op_izq.setTrueLbl(templa)
            self.Op_der.setTrueLbl(self.trueLbl)
            self.Op_izq.falseLbl = self.Op_der.falseLbl = self.falseLbl

        elif self.Operador == '||':
            self.Op_izq.setTrueLbl(self.trueLbl)
            self.Op_der.setTrueLbl(self.trueLbl)
            templa = generador.newLabel()

            self.Op_izq.setFalseLbl(templa)
            self.Op_der.setFalseLbl(self.falseLbl)

        elif self.Operador == '!':
            self.Op_der.setFalseLbl(self.trueLbl)
            self.Op_der.setTrueLbl(self.falseLbl)
            lbnot = self.Op_der.interpretar(tree, table)
            if isinstance(lbnot, Exception): return lbnot

            if lbnot.getTipo() != TIPO.BOOLEAN:
                return Exception("Semantico", "El tipo de la variable debe ser boolean en: ", self.fila, self.columna)

            lbltrue = lbnot.getTrueLbl()
            lblfalse = lbnot.getFalseLbl()
            lbnot.setTrueLbl(lblfalse)
            lbnot.setFalseLbl(lbltrue)
            self.tipo = TIPO.BOOLEAN
            return lbnot
        else:
            return Exception("Semantico", "Los operandos deben ser de tipo BOOLEAN", self.fila, self.columna)

        izq = self.Op_izq.interpretar(tree, table)
        if isinstance(izq, Exception): return izq

        if izq.getTipo() != TIPO.BOOLEAN:
            return Exception("Semantico", "Los operandos deben ser de tipo BOOLEAN en: ", self.fila, self.columna)

        generador.putLabel(templa)
        der = self.Op_der.interpretar(tree, table)
        if isinstance(der, Exception): return der

        if der.getTipo() != TIPO.BOOLEAN:
            return Exception("Semantico", "No se puede utilizar la expresion booleana en: ", self.fila, self.columna)

        generador.addComment("Fin de compilacion de Expresion Logica")
        generador.addSpace()

        ret = Auxiliar(None, TIPO.BOOLEAN, False)
        ret.setTrueLbl(self.trueLbl)
        ret.setFalseLbl(self.falseLbl)
        self.tipo = TIPO.BOOLEAN
        return ret

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