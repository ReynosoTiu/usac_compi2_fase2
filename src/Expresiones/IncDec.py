from ..Abstract.abstract import Abstract
from ..Tabla_Simbolos.Exception import Exception
from ..Tabla_Simbolos.simbolo import Simbolo
from ..Abstract.Tipo import TIPO
from ..Tabla_Simbolos.generador import Generador
from ..Abstract.auxiliar import Auxiliar

class IncDec(Abstract):
    def __init__(self, fila, columna, operator, subLeft):
        self.fila = fila
        self.columna = columna
        self.operator = operator
        self.subLeft = subLeft
        self.tipo = None

    def interpretar(self, arbol,tabla):
        genAux = Generador()
        generador = genAux.getInstance()
        generador.addComment("Compilando Incremento - Decremento")

        simbolo = tabla.getTabla(self.subLeft.ide)
        if simbolo == None:
            generador.addComment("Error. Variable no encontrada")
            return Exception("Semantico", "Variable \"" + self.subLeft.ide + "\" no encontrada", self.fila,
                         self.columna)
        if simbolo.type == TIPO.NUMBER:
            temp = generador.addTemp()
            # Obtencion de posicion de la variable
            tempPos = simbolo.pos
            if not simbolo.isGlobal:
                tempPos = generador.addTemp()
                generador.addExp(tempPos, 'P', simbolo.pos, '+')

            generador.getStack(temp, tempPos)
            generador.addComment("Fin de compilacion de Acceso")
            generador.addSpace()

            generador.addExp(temp, temp, 1, '+')
            generador.setStack(tempPos, temp)
            generador.addComment("Finalizando Incremento")

            return Auxiliar(temp, simbolo.type, True)



        # elif self.operator == '--':
        #     if izq.getTipo() == TIPO.NUMBER:
        #         generador.addExp(izq.getValue(), izq.getValue(), 1, '-')
        #         generador.addComment("Finalizando Decremento")
        #         return izq
