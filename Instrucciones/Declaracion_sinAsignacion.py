from TS.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion
from Abstract.NodoAST import NodoAST
from TS.Simbolo import Simbolo
from TS.Tipo import TIPO



class Declaracion_sinAsignacion(Instruccion):
    def __init__(self, tipo, identificador, fila, columna):
        self.identificador = identificador
        self.tipo = tipo
        self.fila = fila
        self.columna = columna
        self.arreglo = False
        

    def interpretar(self, tree, table,gen):
        if self.tipo == TIPO.NULL_:
            self.tipo = TIPO.NULL_

        if self.tipo == None:
            self.tipo = TIPO.ANY
            simbolo = Simbolo(self.identificador, self.tipo,self.arreglo, self.fila, self.columna,table.Size,1)
            result = table.setTabla(simbolo)

            if isinstance(result, Excepcion): return result
            tree.addSim_Tabla([self.identificador,"Variable",self.tipo,table.nombre_Ent,simbolo.posicion,1,self.fila,self.columna])
            return None
        
        if self.tipo == TIPO.NUMBER:
            simbolo = Simbolo(self.identificador, self.tipo,self.arreglo, self.fila, self.columna,table.Size,1)
            result = table.setTabla(simbolo)
            
            if isinstance(result, Excepcion): 
                return result
            
            gen.AddSetStack("int("+str(simbolo.posicion)+")","0")
            gen.AddBr()
            
            tree.addSim_Tabla([self.identificador,"Variable",self.tipo,table.nombre_Ent,simbolo.posicion,1,self.fila,self.fila])
            
            return None
        if self.tipo == TIPO.STRING:
            nuevoTemporal = gen.newTemp()
    
            simbolo = Simbolo(self.identificador, self.tipo,self.arreglo, self.fila, self.columna,table.Size,1)
            
            result = table.setTabla(simbolo)
            if isinstance(result, Excepcion): 
                return result
           
            gen.AddAssign(nuevoTemporal,"H")

            gen.AddSetHeap("int(H)","34")
            gen.AddExpression("H", "H", "1", "+")
            gen.AddSetHeap("int(H)","34")
            gen.AddExpression("H", "H", "1", "+")
            gen.AddSetHeap("int(H)", "-1")
            gen.AddExpression("H", "H", "1", "+")
            gen.AddBr()
            
            gen.AddSetStack("int("+str(simbolo.posicion)+")",nuevoTemporal)

            tree.addSim_Tabla([self.identificador,"Variable",self.tipo,table.nombre_Ent,simbolo.posicion,1,self.fila,self.columna])
            
            return None
        if self.tipo == TIPO.BOOLEAN:
            simbolo = Simbolo(self.identificador, self.tipo,self.arreglo, self.fila, self.columna,table.Size,1)
            result = table.setTabla(simbolo)

            if isinstance(result, Excepcion): return result
            gen.AddSetStack("int("+str(simbolo.posicion)+")","0")
            gen.AddBr()
            tree.addSim_Tabla([self.identificador,"Variable",self.tipo,table.nombre_Ent,simbolo.posicion,1,self.fila,self.columna])
            return None
        
        return Excepcion("Semantico","Error Tipo de Dato no encontrado"+str(self.tipo),self.fila,self.columna)


        
    
    def getNodo(self):
        nodo = NodoAST("DECLARACION_SINAGNACION")
        nodo.agregarHijo(str(self.tipo))
        nodo.agregarHijo(str(self.identificador))
        return nodo
