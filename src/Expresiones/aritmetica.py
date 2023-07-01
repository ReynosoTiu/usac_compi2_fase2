from ..Abstract.abstract import Abstract
from ..Abstract.Tipo import TIPO
from ..Abstract.auxiliar import Auxiliar
from ..Tabla_Simbolos.Exception import Exception
from ..Tabla_Simbolos.generador import Generador
from ..Instrucciones.Llamada import Llamada

class Aritmetica(Abstract):

    def __init__(self, op_izq, op_der, op, fila, columna):
        self.op_izq = op_izq # <<Class.Primitivos>>
        self.op_der = op_der # <<Class.Primitivos>>
        self.op = op # *
        self.tipo = None
        super().__init__(fila, columna)
    
    def interpretar(self, tree, table):
        genAux = Generador()
        generador = genAux.getInstance()

        izq = self.op_izq.interpretar(tree, table)  # devuelve objeto de tipo auxiliar
        if isinstance(izq, Exception): return izq
        if isinstance(self.op_der, Llamada):
            self.op_der.guardarTemps(generador, table, [izq.getValue()])
            der = self.op_der.interpretar(tree, table)
            if isinstance(der, Exception): return der
            self.op_der.recuperarTemps(generador, table, [izq.getValue()])
        else:
            der = self.op_der.interpretar(tree, table)  # devuelve objeto de tipo auxiliar
            if isinstance(der, Exception): return der


        # SUMA
        if self.op == '+':
            # Si izq es entero o flotante y derecha es entero o flotante
            if ((izq.getTipo() or izq.getTipoAux()) and (der.getTipo() or der.getTipoAux())) == TIPO.NUMBER:
                self.tipo = TIPO.NUMBER
                temporal = generador.addTemp()
                generador.addExp(temporal, izq.getValue(), der.getValue(), self.op)
                return Auxiliar(temporal, self.tipo, True)
            elif ((izq.getTipo() or izq.getTipoAux()) and (der.getTipo() or der.getTipoAux())) == TIPO.STRING:
                self.tipo = TIPO.STRING
                temporal = generador.addTemp()
                generador.addAsig(temporal, 'H')
                # agregando cadena del operador izq
                returnLbl = generador.newLabel() # Label para salir de la funcion
                compareLbl = generador.newLabel() # Label para la comparacion para buscar fin de cadena
                tempH = izq.getValue()
                generador.putLabel(compareLbl)
                generador.addIdent()
                tempC = generador.addTemp() # Temporal para comparar
                generador.getHeap(tempC, tempH)
                generador.addIdent()
                generador.addIf(tempC, '-1', '==', returnLbl)
                generador.addIdent()
                generador.setHeap('H', tempC)
                generador.nextHeap()
                generador.addIdent()
                generador.addExp(tempH, tempH, '1', '+')
                generador.addIdent()
                generador.addGoto(compareLbl)
                generador.putLabel(returnLbl)
                # agregando cadena del operador derecho
                returnLbl = generador.newLabel()  # Label para salir de la funcion
                compareLbl = generador.newLabel()  # Label para la comparacion para buscar fin de cadena
                tempH = der.getValue()
                generador.putLabel(compareLbl)
                generador.addIdent()
                tempC = generador.addTemp() # Temporal para comparar
                generador.getHeap(tempC, tempH)
                generador.addIdent()
                generador.addIf(tempC, '-1', '==', returnLbl)
                generador.addIdent()
                generador.setHeap('H', tempC)
                generador.nextHeap()
                generador.addIdent()
                generador.addExp(tempH, tempH, '1', '+')
                generador.addIdent()
                generador.addGoto(compareLbl)
                generador.putLabel(returnLbl)
                generador.setHeap('H', -1)  # simular un fin de cadena con -1
                generador.nextHeap()
                return Auxiliar(temporal, self.tipo, True)
            elif isinstance(izq.getValue(), str) and (isinstance(der.getValue(), int) or isinstance(der.getValue(), float)):
                # Agregar a tabla de errores
                return Exception("Semantico", "No se puede sumar un string con un number", self.fila, self.columna)
            elif (isinstance(izq.getValue(), int) or isinstance(izq.getValue(), float)) and isinstance(der.getValue(), str):
                # Agregar a tabla de errores
                return Exception("Semantico", "No se puede sumar un number con un string", self.fila, self.columna)
            else:
                return Exception("Semantico", "Tipo de dato invalido en suma", self.fila, self.columna)
        # RESTA
        elif self.op == '-':
            if (izq.getTipo() and der.getTipo()) == TIPO.NUMBER:
                self.tipo = TIPO.NUMBER
                temporal = generador.addTemp()
                generador.addExp(temporal, izq.getValue(), der.getValue(), self.op)
                return Auxiliar(temporal, self.tipo, True)
            else:
                return Exception("Semantico", "Los operandos deben ser numeros para la resta", self.fila, self.columna)
        # MULTIPLICACION
        elif self.op == '*':
            if (izq.getTipo() and der.getTipo()) == TIPO.NUMBER:
                self.tipo = TIPO.NUMBER
                temporal = generador.addTemp()
                generador.addExp(temporal, izq.getValue(), der.getValue(), self.op)
                return Auxiliar(temporal, self.tipo, True)
            else:
                return Exception("Semantico", "Los factores deben ser numeros para la multiplicacion", self.fila,
                             self.columna)
        # DIVISION
        elif self.op == '/':
            if (izq.getTipo() and der.getTipo()) == TIPO.NUMBER:
                self.tipo = TIPO.NUMBER
                generador.addComment("-----DIVISION-----")
                trueLbl = generador.newLabel()
                returnLbl = generador.newLabel()
                generador.addIf(der.getValue(), 0, '!=', trueLbl)
                # en caso de ser falso o == a 0
                generador.addMathErr()
                temp = generador.addTemp()
                generador.addAsig(temp, 0)
                generador.addGoto(returnLbl)
                generador.putLabel(trueLbl)
                generador.addExp(temp, izq.getValue(), der.getValue(), '/')
                generador.putLabel(returnLbl)
                return Auxiliar(temp, self.tipo, True)

            else:
                return Exception("Semantico", "Los operandos deben ser numeros para la division", self.fila, self.columna)
        elif self.op == '%':
            if (izq.getTipo() and der.getTipo()) == TIPO.NUMBER:
                self.tipo = TIPO.NUMBER
                generador.addComment("-----MODULO-----")
                trueLbl = generador.newLabel()
                returnLbl = generador.newLabel()
                generador.addIf(der.getValue(), 0, '!=', trueLbl)
                # en caso de ser falso o == a 0
                generador.addMathErr()
                temp = generador.addTemp()
                generador.addAsig(temp, 0)
                generador.addGoto(returnLbl)
                generador.putLabel(trueLbl)
                # self.codeIn(f'{result} = {left} {op} {right};\n')
                generador.addExp(temp, f'float64(int({izq.getValue()})', f'int({der.getValue()}))', '%')
                generador.putLabel(returnLbl)
                return Auxiliar(temp, self.tipo, True)
        elif self.op == '^':
            if (izq.getTipo() and der.getTipo()) == TIPO.NUMBER:
                self.tipo = TIPO.NUMBER
                temporal = generador.addTemp()
                generador.addPotencia(temporal, izq.getValue(), der.getValue())
                return Auxiliar(temporal, self.tipo, True)
            else:
                return Exception("Semantico", "Los operandos deben ser numeros para la division", self.fila, self.columna)
           
   

    def getTipo(self):
        return self.tipo