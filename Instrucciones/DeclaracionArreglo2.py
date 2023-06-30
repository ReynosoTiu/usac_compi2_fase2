from Expresiones.Identificador import Identificador
from Abstract.Instruccion import Instruccion
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.Simbolo import Simbolo
from TS.Tipo import TIPO
import copy
from re import A

class DeclaracionArreglo2(Instruccion):
    def __init__(self, tipo1, dimensiones, identificador,Lexpresiones, fila, columna):
        #let id = [1,2,3]
        #let id : number = [1,2,3,4]
        self.identificador = identificador
        self.tipo = tipo1
        self.dimensiones = dimensiones
        self.Lexpresiones = Lexpresiones
        self.fila = fila
        self.columna = columna
        self.arreglo = True


    def interpretar(self, tree, table,gen):
        #if self.tipo != self.tipo2:                     #VERIFICACION DE TIPOS
        #    return Excepcion("Semantico", "Tipo de dato diferente en Arreglo.", self.fila, self.columna)
        
        #if self.dimensiones != len(self.Lexpresiones):   #VERIFICACION DE DIMENSIONES
        #    return Excepcion("Semantico", "Dimensiones diferentes en Arreglo.", self.fila, self.columna)
        if isinstance(self.Lexpresiones,Identificador):
            datoObtenido = self.Lexpresiones.interpretar(tree,table)
            if isinstance(datoObtenido,Excepcion): return datoObtenido
            simbolo = Simbolo(str(self.identificador).lower(), self.tipo, self.arreglo, self.fila, self.columna,datoObtenido)
            result = table.setTabla(simbolo)
            if isinstance(result, Excepcion): return result
            return None
                    
        #_______________________ OBTENER TAMANIOS VECTOR_________________________
        vect_tam = []
        if self.dimensiones == 1:
            vect_tam.append(len(self.Lexpresiones))
        elif self.dimensiones == 2:
            vect_tam.append(len(self.Lexpresiones))
            vect_tam.append(len(self.Lexpresiones[0]))
        elif self.dimensiones == 3:
            vect_tam.append(len(self.Lexpresiones))
            vect_tam.append(len(self.Lexpresiones[0]))
            vect_tam.append(len(self.Lexpresiones[0][0]))

        # CREACION DEL ARREGLO
        value = self.crearDimensiones(tree, table, copy.copy(vect_tam))     #RETORNA EL ARREGLO DE DIMENSIONES
        if isinstance(value, Excepcion): return value
        #_______________________ 1 DIMENSION __________________________
        if self.dimensiones == 1:
            for i in range(len(self.Lexpresiones)):
                bu = self.Lexpresiones[i].interpretar(tree,table)
                if isinstance(bu,Excepcion): return bu
                if self.tipo == TIPO.ANY:
                    #self.tipo == self.Lexpresiones[i].tipo
                    value[i] = self.Lexpresiones[i].interpretar(tree,table)
                else:
                    tree.updateConsola("Error Semantico tipos "+str(self.tipo)+" != "+str(self.Lexpresiones[i].tipo))
                    
        #_______________________ 2 DIMENSIONES _________________________
        if self.dimensiones == 2:
            for i in range(len(self.Lexpresiones)):
                for j in range(len(self.Lexpresiones[0])):
                    value[i][j]= self.Lexpresiones[i][j].interpretar(tree,table)
        
        #_______________________ 3 DIMENSIONES _________________________
        if self.dimensiones == 3:
            for i in range(len(self.Lexpresiones)):
                for j in range(len(self.Lexpresiones[0])):
                    for k in range(len(self.Lexpresiones[0][0])):
                        value[i][j][k]= self.Lexpresiones[i][j][k].interpretar(tree,table)
                        

        simbolo = Simbolo(self.identificador, self.tipo, self.arreglo, self.fila, self.columna, value)
        result = table.setTabla(simbolo)
        if isinstance(result, Excepcion): return result
        tree.addSim_Tabla([self.identificador,"Arreglo",str(self.tipo),table.nombre_Ent,value,self.fila,self.fila])
        return None
        

    def getNodo(self):
        nodo = NodoAST("DECLARACION ARREGLO")
        nodo.agregarHijo(str(self.tipo))
        nodo.agregarHijo(str(self.dimensiones))
        nodo.agregarHijo(str(self.identificador))
        #nodo.agregarHijo(str(self.tipo2))

        exp = NodoAST("LISTA EXPRESIONES")
        if isinstance(self.Lexpresiones,Identificador):
            exp.agregarHijoNodo(self.Lexpresiones.getNodo())
            nodo.agregarHijoNodo(exp)
            return nodo

        if self.dimensiones == 1:
            for expresion in self.Lexpresiones:
                exp.agregarHijoNodo(expresion.getNodo())

        elif self.dimensiones == 2:
            for expresion in self.Lexpresiones:
                for expresion2 in expresion:
                    exp.agregarHijoNodo(expresion2.getNodo())

        elif self.dimensiones == 3:
            for expresion in self.Lexpresiones:
                for expresion2 in expresion:
                    for expresion3 in expresion2:
                        exp.agregarHijoNodo(expresion3.getNodo())
            

        nodo.agregarHijoNodo(exp)
        return nodo

    
    def crearDimensiones(self, tree, table, Lexpresiones):
        arr = []
        if len(Lexpresiones) == 0:
            return None
        dimension = Lexpresiones.pop(0)
        num = dimension #dimension.interpretar(tree, table,jconsola)
        if isinstance(num, Excepcion): return num
        #if dimension.tipo != TIPO.ENTERO:
        #    return Excepcion("Semantico", "Expresion diferente a ENTERO en Arreglo.", self.fila, self.columna)
        contador = 0
        while contador < num:
            arr.append(self.crearDimensiones(tree, table, copy.copy(Lexpresiones)))
            contador += 1
        return arr
    
