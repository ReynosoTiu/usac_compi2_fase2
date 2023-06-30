from Abstract.NodoAST import NodoAST
from Abstract.Instruccion import Instruccion
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO, OperadorLogico

class Casteo(Instruccion):
    def __init__(self, tipo, expresion, fila, columna):
        self.expresion = expresion
        self.fila = fila
        self.columna = columna
        self.tipo = tipo
        self.arreglo = False

    
    def interpretar(self, tree, table,gen):
        val = self.expresion.interpretar(tree, table,gen)
        if self.tipo == TIPO.DECIMAL:
            if self.expresion.tipo == TIPO.NUMBER:
                try:
                    return float(self.obtenerVal(self.expresion.tipo, val))
                except:
                    return Excepcion("Semantico", "No se puede castear para Float. entero", self.fila, self.columna)
            elif self.expresion.tipo == TIPO.CADENA:
                try:
                    return float(self.obtenerVal(self.expresion.tipo, val))
                except:
                    return Excepcion("Semantico", "No se puede castear para Float Cadena.", self.fila, self.columna)
            elif self.expresion.tipo == TIPO.CHARACTER:
                try:
                    return float(ord(self.obtenerVal(self.expresion.tipo,val)))
                except:
                    return Excepcion("Semantico", "No se puede castear para Float Char.", self.fila, self.columna)

            return Excepcion("Semantico", "Tipo Erroneo de casteo para Double.", self.fila, self.columna)
        if self.tipo == TIPO.NUMBER:
            if self.expresion.tipo == TIPO.DECIMAL:
                try:
                    return int(self.obtenerVal(self.expresion.tipo, val))
                except:
                    return Excepcion("Semantico", "No se puede castear para Int. en decimal", self.fila, self.columna)
            elif self.expresion.tipo == TIPO.CADENA:
                try:
                    return int(self.obtenerVal(self.expresion.tipo, val))
                except:
                    return Excepcion("Semantico", "No se puede castear para Int en cadena.", self.fila, self.columna)
            elif self.expresion.tipo == TIPO.CHARACTER:
                try:
                    return int(ord(self.obtenerVal(self.expresion.tipo,val)))
                except:
                    return Excepcion("Semantico", "No se puede castear para Int en caracter.", self.fila, self.columna)

            return Excepcion("Semantico", "Tipo Erroneo de casteo para Int.", self.fila, self.columna)
        if self.tipo == TIPO.CADENA:
            if self.expresion.tipo == TIPO.DECIMAL:
                try:
                    return str(self.obtenerVal(self.expresion.tipo, val))
                except:
                    return Excepcion("Semantico", "No se puede castear para String. en decimal", self.fila, self.columna)
            if self.expresion.tipo == TIPO.NUMBER:
                try:
                    return str(self.obtenerVal(self.expresion.tipo, val))
                except:
                    return Excepcion("Semantico", "No se puede castear para String. en entero", self.fila, self.columna)
            return Excepcion("Semantico", "Tipo Erroneo de casteo para String.", self.fila, self.columna)
            
        if self.tipo == TIPO.CHARACTER:
            if self.expresion.tipo == TIPO.NUMBER:
                try:
                    return chr(self.obtenerVal(self.expresion.tipo, val))
                except:
                    return Excepcion("Semantico", "No se puede castear para caracter.", self.fila, self.columna)
            return Excepcion("Semantico", "Tipo Erroneo de casteo para Caracter.", self.fila, self.columna)
        if self.tipo == TIPO.BOOLEAN:
            if self.expresion.tipo == TIPO.CADENA:
                try:
                    if self.obtenerVal(self.expresion.tipo, val).lower() == "true":
                        return True
                    elif self.obtenerVal(self.expresion.tipo, val).lower() == "false":
                        return False
                except:
                    return Excepcion("Semantico", "No se puede castear para booleano. con string", self.fila, self.columna)
            return Excepcion("Semantico", "Tipo Erroneo de casteo para Caracter.", self.fila, self.columna)
        return Excepcion("Semantico", "Tipo "+str(self.tipo)+" No Forma Parte de Casteo.", self.fila, self.columna)


        
    def getNodo(self):
        nodo = NodoAST("CASTEO")
        nodo.agregarHijo(str(self.tipo))
        nodo.agregarHijoNodo(self.expresion.getNodo())
        return nodo

    def obtenerVal(self, tipo, val):
        if tipo == TIPO.NUMBER:
            return float(val)
        elif tipo == TIPO.BOOLEAN:
            if val.lower() == 'true':
                return True
            return False
        return str(val)