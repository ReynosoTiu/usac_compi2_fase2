from ..Abstract.abstract import Abstract
from ..Tabla_Simbolos.Exception import Exception
from ..Tabla_Simbolos.tabla_simbolos import TablaSimbolos
from ..Instrucciones.Return import Return
from ..Tabla_Simbolos.simbolo import Simbolo
from ..Abstract.Tipo import TIPO
from ..Tabla_Simbolos.generador import Generador
from ..Abstract.auxiliar import Auxiliar

class Llamada(Abstract):
    def __init__(self, identificador, parametros, fila, columna):
        self.identificador = identificador
        self.parametros = parametros
        self.trueLbl = ''
        self.falseLbl = ''
        super().__init__(fila, columna)

    def interpretar(self, arbol, tabla):
        genAux = Generador()
        generador = genAux.getInstance()
        funcion = arbol.getFuncion(self.identificador)

        if funcion != None:
            generador.addComment(f'Llamada a la funcion {self.identificador}')
            paramValues = []
            temps = []
            size = tabla.size

            if self.parametros is not None:
                for parametros in self.parametros:
                    if isinstance(parametros, Llamada):
                        self.guardarTemps(generador, tabla, temps)
                        a = parametros.interpretar(arbol, tabla)
                        if isinstance(a, Exception): return a
                        paramValues.append(a)
                        self.recuperarTemps(generador, tabla, temps)
                    else:
                        value = parametros.interpretar(arbol, tabla)
                        if isinstance(value, Exception): return value
                        paramValues.append(value)
                        temps.append(value.getValue())

            temp = generador.addTemp()

            generador.addExp(temp, 'P', size + 1, '+')
            aux = 0

            if self.parametros is not None:
                if len(funcion.getParams()) == len(paramValues):
                    for param in paramValues:
                        if funcion.parametros[aux]['tipo'] == param.getTipo():
                            aux += 1
                            generador.setStack(temp, param.getValue())
                            if aux != len(paramValues):
                                generador.addExp(temp, temp, 1, '+')
                        else:
                            generador.addComment(
                                f'Fin de la llamada a la funcion {self.identificador} por error, consulte la lista de errores')
                            return Exception("Semantico",
                                         f"El tipo de dato de los parametros no coincide con la funcion {self.identificador}",
                                         self.fila, self.columna)

            generador.newEnv(size)
            # self.getFuncion(funcion, arbol, tabla) # Sirve para llamar a una funcion nativa
            generador.callFun(funcion.identificador)
            generador.getStack(temp, 'P')
            generador.retEnv(size)
            generador.addComment(f'Fin de la llamada a la funcion {self.identificador}')
            generador.addSpace()

            if funcion.getTipo() != TIPO.BOOLEAN:
                return Auxiliar(temp, funcion.getTipo(), True)
            else:
                generador.addComment('Recuperacion de booleano')
                if self.trueLbl == '':
                    self.trueLbl = generador.newLabel()
                if self.falseLbl == '':
                    self.falseLbl = generador.newLabel()
                generador.addIf(temp, 1, '==', self.trueLbl)
                generador.addGoto(self.falseLbl)
                ret = Return(temp, funcion.getTipo(), True)
                ret.trueLbl = self.trueLbl
                ret.falseLbl = self.falseLbl
                generador.addComment('Fin de recuperacion de booleano')
                return ret

    def guardarTemps(self, generador, tabla, tmp2):
        generador.addComment('Guardando temporales')
        tmp = generador.addTemp()
        for tmp1 in tmp2:
            generador.addExp(tmp, 'P', tabla.size, '+')
            generador.setStack(tmp, tmp1)
            tabla.size += 1
        generador.addComment('Fin de guardado de temporales')

    def recuperarTemps(self, generador, tabla, tmp2):
        generador.addComment('Recuperando temporales')
        tmp = generador.addTemp()
        for tmp1 in tmp2:
            tabla.size -= 1
            generador.addExp(tmp, 'P', tabla.size, '+')
            generador.getStack(tmp1, tmp)
        generador.addComment('Fin de recuperacion de temporales')