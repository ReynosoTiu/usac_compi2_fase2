
from Abstract.Instruccion import Instruccion
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.Simbolo import Simbolo
from TS.Tipo import TIPO
import copy
from re import A

class DeclaracionArreglo(Instruccion):
    def __init__(self,identificador,tipo,expresiones, fila, columna):
        self.identificador = identificador
        self.tipo = tipo
        self.expresiones = expresiones
        self.fila = fila
        self.columna = columna
        self.arreglo = True


    def interpretar(self, tree, table,gen):
        
        # CREACION DEL ARREGLO
        value = self.crearDimensiones(tree, table, copy.copy(self.expresiones))     #RETORNA EL ARREGLO DE DIMENSIONES
        if isinstance(value, Excepcion): 
            return value
        
        simbolo = Simbolo(self.identificador, self.tipo, self.arreglo, self.fila, self.columna, value)
        result = table.setTabla(simbolo)
        if isinstance(result, Excepcion): 
            return result

        tree.addSim_Tabla([self.identificador,"Arreglo",str(self.tipo),table.nombre_Ent,value,self.fila,self.fila])
        return None

    def getNodo(self):
        nodo = NodoAST("DECLARACION ARREGLO")
        nodo.agregarHijo(str(self.tipo))
        nodo.agregarHijo(str(len(self.expresiones)))
        nodo.agregarHijo(str(self.identificador))
        exp = NodoAST("EXPRESIONES DE LAS DIMENSIONES")
        for expresion in self.expresiones:
            exp.agregarHijoNodo(expresion.getNodo())
        nodo.agregarHijoNodo(exp)
        return nodo

    def crearDimensiones(self, tree, table, expresiones):
        arr = []
        if len(expresiones) == 0:
            return None
        dimension = expresiones.pop(0)
        num = dimension.interpretar(tree, table)
        if isinstance(num, Excepcion): 
            return num
        if dimension.tipo != TIPO.NUMBER:
            return Excepcion("Semantico", "Expresion diferente a ENTERO en Arreglo.", self.fila, self.columna)
        contador = 0
        while contador < num:
            arr.append(self.crearDimensiones(tree, table, copy.copy(expresiones)))
            contador += 1
        return arr



            

