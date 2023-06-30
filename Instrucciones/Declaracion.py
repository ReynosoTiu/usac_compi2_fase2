from TS.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion
from Abstract.NodoAST import NodoAST
from TS.Simbolo import Simbolo
from TS.Tipo import TIPO


class Declaracion(Instruccion):
    def __init__(self, tipo, identificador, fila, columna, expresion=None):
        self.identificador = identificador
        self.tipo = tipo
        self.expresion = expresion
        self.fila = fila
        self.columna = columna
        self.arreglo = False

    def interpretar(self, tree, table,gen):
        
        if self.tipo == None:
            self.tipo = TIPO.ANY
    
        value = self.expresion.interpretar(tree, table,gen) # Valor a asignar a la variable
        
        if isinstance(value, Excepcion): 
            return value

        if self.tipo == TIPO.NULL_:
            simbolo = Simbolo(str(self.identificador), self.expresion.tipo,self.expresion.arreglo,self.fila, self.columna,table.Size,1)
            result = table.setTabla(simbolo)

            if isinstance(result, Excepcion): return result
            tree.addSim_Tabla([self.identificador,"Variable",str(self.expresion.tipo),table.nombre_Ent,simbolo.posicion,1,self.fila,self.columna])
            return None

        if self.tipo == TIPO.ANY:
            simbolo = Simbolo(self.identificador, self.tipo,self.expresion.arreglo,self.fila, self.columna,table.Size,1)
            result = table.setTabla(simbolo)

            if isinstance(result, Excepcion): return result
            tree.addSim_Tabla([self.identificador,"Variable",str(self.tipo),table.nombre_Ent,simbolo.posicion,1,self.fila,self.columna])
            return None

        if self.tipo == TIPO.NUMBER:
            simbolo = Simbolo(self.identificador, self.tipo,self.expresion.arreglo,self.fila, self.columna,table.Size,1)
            
            result = table.setTabla(simbolo)
            if isinstance(result, Excepcion): return result
            
            gen.AddSetStack("int("+str(simbolo.posicion)+")",value.valor)
            gen.AddBr()

            tree.addSim_Tabla([self.identificador,"Variable",str(self.tipo),table.nombre_Ent,simbolo.posicion,1,self.fila,self.columna])
            return None

        if self.tipo == TIPO.STRING:
            simbolo = Simbolo(self.identificador, self.tipo,self.expresion.arreglo,self.fila, self.columna,table.Size,1)
            
            result = table.setTabla(simbolo)
            if isinstance(result, Excepcion): return result
            
            gen.AddSetStack("int("+str(simbolo.posicion)+")",value.valor)
            gen.AddBr()

            tree.addSim_Tabla([self.identificador,"Variable",str(self.tipo),table.nombre_Ent,simbolo.posicion,1,self.fila,self.columna])
            return None
        
        if self.tipo == TIPO.BOOLEAN:
            simbolo = Simbolo(self.identificador, self.tipo,self.expresion.arreglo,self.fila, self.columna,table.Size,1)
            
            result = table.setTabla(simbolo)
            if isinstance(result, Excepcion):
                return result
            
            #si no es temporal (valor booleano)
            newLabel = gen.newLabel()
            #add true labels
            for i in range(len(value.TrueLvl)):
                gen.AddLabel(value.TrueLvl[i])

            gen.AddSetStack("int("+str(simbolo.posicion)+")","1")
            gen.AddGoto(newLabel)
            
            #add false labels
            for i in range(len(value.FalseLvl)):
                gen.AddLabel(value.FalseLvl[i])
            
            gen.AddSetStack("int("+str(simbolo.posicion)+")","0")
            gen.AddGoto(newLabel)
            gen.AddLabel(newLabel)
            gen.AddBr()

            tree.addSim_Tabla([self.identificador,"Variable",str(self.tipo),table.nombre_Ent,simbolo.posicion,1,self.fila,self.columna])
            return None
        

        return Excepcion("Semantico", "Tipo de dato diferente en Declaracion", self.fila, self.columna)
        
    
    def getNodo(self):
        nodo = NodoAST("DECLARACION")
        nodo.agregarHijo(str(self.expresion.tipo))
        nodo.agregarHijo(str(self.identificador))
        nodo.agregarHijoNodo(self.expresion.getNodo())
        return nodo
