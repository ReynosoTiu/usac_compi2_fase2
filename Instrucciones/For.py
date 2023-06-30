from Abstract.Instruccion import Instruccion
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break
from Instrucciones.Continue import Continue
from Instrucciones.Return import Return

class For(Instruccion):
    def __init__(self,declaracion,condicion,incremento,instrucciones,fila,columna):
        self.declaracion = declaracion
        self.condicion = condicion
        self.incremento =  incremento
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table,gen):
        
        declaracion_ = self.declaracion.interpretar(tree,table,gen)
        if isinstance(declaracion_,Excepcion):
            return declaracion_
        newLabelRetorno = gen.newLabel()
        gen.AddLabel(newLabelRetorno)

        condicion_ = self.condicion.interpretar(tree,table,gen)
        if isinstance(condicion_,Excepcion):
            return condicion_
        gen.AddComment("====================    GENERANDO FOR   ====================")
        
        for i in range(len(condicion_.TrueLvl)):
            gen.AddLabel(condicion_.TrueLvl[i])
        #ejecutando instrucciones
        tablaFor = TablaSimbolos(table,"FOR")
        for instruccion in self.instrucciones:
            instruccion.interpretar(tree,tablaFor,gen)
            #Aqui varificar si es break o instance xD
            #retorno
        es_incremento = self.incremento.interpretar(tree,tablaFor,gen)
        if isinstance(es_incremento,Excepcion):
            return es_incremento
        gen.AddGoto(newLabelRetorno)
        #agregando etiquetas falsas
        for i in range(len(condicion_.FalseLvl)):
            gen.AddLabel(condicion_.FalseLvl[i])
        return None #Cero errores
    
    def getNodo(self):
        nodo = NodoAST("FOR")
        nodo.agregarHijoNodo(self.declaracion.getNodo())
        nodo.agregarHijoNodo(self.condicion.getNodo())
        nodo.agregarHijoNodo(self.incremento.getNodo())

        instrucciones = NodoAST("INSTRUCCIONES FOR")
        for instr in self.instrucciones:
            instrucciones.agregarHijoNodo(instr.getNodo())
        nodo.agregarHijoNodo(instrucciones)
        return nodo