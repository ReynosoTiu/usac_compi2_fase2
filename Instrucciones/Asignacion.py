from TS.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion
from Abstract.NodoAST import NodoAST
from TS.Simbolo import Simbolo
from TS.Tipo import TIPO


class Asignacion(Instruccion):
    def __init__(self, identificador, expresion, fila, columna):
        self.identificador = identificador
        self.expresion = expresion
        self.fila = fila
        self.columna = columna
        self.arreglo = False
        

    def interpretar(self, tree, table,gen):

        value = self.expresion.interpretar(tree, table,gen) # Valor a asignar a la variable

        if isinstance(value, Excepcion): 
            return value
        #   Aqui se obtiene el simbolo necesitamos recuperar la posicion de la variable original
        simbolo = table.getTabla(self.identificador)

        if simbolo == None:
            return Excepcion("Semantico","Error la variable"+str(self.identificador)+" no existe",self.fila,self.columna)
        if value.tipo == TIPO.BOOLEAN:
            newLvlSalida = gen.newLabel()
            gen.AddComment("=================== ASIGNACION BOOL ===================")
            for i in value.TrueLvl:
                gen.AddLabel(i)
            gen.AddSetStack("int("+str(simbolo.posicion)+")","1")
            gen.AddGoto(newLvlSalida)
           
            for i in value.FalseLvl:
                gen.AddLabel(i)
            gen.AddSetStack("int("+str(simbolo.posicion)+")","0")
            gen.AddLabel(newLvlSalida)
            gen.AddBr()
            return None
        if value.tipo == TIPO.STRING:
            gen.AddComment("=================== ASIGNACION STRING ===================")
            gen.AddSetStack("int("+str(simbolo.posicion)+")",value.valor)
            gen.AddBr()
            return None
        
        if value.tipo == TIPO.NUMBER:
            gen.AddComment("=================== ASIGNACION NUMBER ===================")
            gen.AddSetStack("int("+str(simbolo.posicion)+")",value.valor)
            gen.AddBr()
            return None

        
        
        #tree.actualizarSim_Tabla_reporte(self.identificador,table)
        return Excepcion("Semantico","Error "+str(value.tipo)+" no existe",self.fila,self.columna)
    
    def getNodo(self):
        nodo = NodoAST("ASIGNACION")
        nodo.agregarHijo(str(self.identificador))
        nodo.agregarHijoNodo(self.expresion.getNodo())
        return nodo
