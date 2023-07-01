from typing import List
from ..Abstract.abstract import Abstract
from ..Tabla_Simbolos.Exception import Exception
from ..Tabla_Simbolos.tabla_simbolos import TablaSimbolos
from ..Instrucciones.Return import Return
from ..Tabla_Simbolos.generador import Generador
from ..Abstract.Tipo import TIPO
class Function(Abstract):
    def __init__(self, identificador, parametros, instrucciones, fila, columna, tipo_funcion):
        self.identificador = identificador
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.tipo = tipo_funcion
        #self.tipo_funcion = tipo_funcion
        self.recTemp = True
        super().__init__(fila, columna)


    def interpretar(self, arbol, tabla):
        funcion = arbol.setFunciones(self.identificador, self)
        if isinstance(funcion, Exception): return funcion

        genAux = Generador()
        generador = genAux.getInstance()
        generador.addComment(f'Compilacion de la funcion {self.identificador}')

        entorno = TablaSimbolos(tabla, "FUNCION")

        Lblreturn = generador.newLabel()
        entorno.returnLbl = Lblreturn
        entorno.size = 1

        if self.parametros != None:
            for parametro in self.parametros:
                if parametro['tipo'] == 'struct':
                    simbolo = entorno.setTabla(parametro['id'], parametro['tipo'], True)
                elif not isinstance(parametro['tipo'], List):
                    simbolo = entorno.setTabla(parametro['id'], parametro['tipo'], (
                                parametro['tipo'] == 'string' or parametro['tipo'] == 'array' or parametro[
                            'tipo'] == 'struct'))
                else:
                    simbolo = entorno.setTabla(parametro['id'], parametro['tipo'][0], True)
                    simbolo.setTipoAux(parametro['tipo'][1])
                    if parametro['tipo'][0] == 'struct':
                        struct = arbol.getStruct(parametro['tipo'][1])
                        simbolo.setParams(struct.getParams())

        generador.addBeginFunc(self.identificador)

        for instruccion in self.instrucciones:
            value = instruccion.interpretar(arbol, entorno)
            if isinstance(value, Exception):
                arbol.setErrores(value)
            if isinstance(value, Return):
                if value.expresion is None:
                    generador.addComment('Retorno sin valor')
                    generador.addGoto(entorno.returnLbl)
                elif value.getTrueLbl() == '':
                    generador.addComment('Resultado a retornar en la funcion')
                    generador.setStack('P', value.getValor())
                    generador.addGoto(entorno.returnLbl)
                    generador.addComment('Fin del resultado a retornar')
                else:
                    generador.addComment('Resultado a retornar en la funcion')
                    generador.putLabel(value.getTrueLbl())
                    generador.setStack('P', '1')
                    generador.addGoto(entorno.returnLbl)
                    generador.putLabel(value.getFalseLbl())
                    generador.setStack('P', '0')
                    generador.addGoto(entorno.returnLbl)
                    generador.addComment('Fin del resultado a retornar')

        generador.addGoto(Lblreturn)
        generador.putLabel(Lblreturn)

        generador.addComment(f'Fin de la compilacion de la funcion {self.identificador}')
        generador.addEndFunc()
        generador.addSpace()
        return

    def getParams(self):
        return self.parametros

    def getTipo(self):
        return self.tipo