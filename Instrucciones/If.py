from Abstract.Instruccion import Instruccion
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break
from Instrucciones.Continue import Continue
from Instrucciones.Return import Return


class If(Instruccion):
    def __init__(self, condicion, instruccionesIf, instruccionesElse, ElseIf, fila, columna):
        self.condicion = condicion
        self.instruccionesIf = instruccionesIf
        self.instruccionesElse = instruccionesElse
        self.elseIf = ElseIf
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table,gen):
        gen.AddComment("==================  GENERANDO IF    ====================")
        condicion_v = self.condicion.interpretar(tree,table,gen)
        newLabel = gen.newLabel()#etiqueta de salida

        if condicion_v.tipo == TIPO.BOOLEAN:
            #agregando etiquetas verdaderas
            for i in range(len(condicion_v.TrueLvl)):
                gen.AddLabel(condicion_v.TrueLvl[i])

            #instrucción del IF
            if self.instruccionesIf != None:
                tablaIf = TablaSimbolos(table,"IF")
                for instruccion in self.instruccionesIf:
                    instruccion.interpretar(tree,tablaIf,gen)
                #etiqueta salida
                gen.AddGoto(newLabel)
            #agregando etiquetas falsas
            for i in range(len(condicion_v.FalseLvl)):
                gen.AddLabel(condicion_v.FalseLvl[i])

            #instrucción del else
            if self.instruccionesElse != None:
                tablaElse = TablaSimbolos(table,"ELSE")
                for ins_else in self.instruccionesElse:
                    ins_else.interpretar(tree,tablaElse,gen)
                #etiqueta salida
                gen.AddLabel(newLabel)
                return None
            if self.elseIf != None:
                Retorno = self.elseIf.interpretar(tree,table,gen)
                if isinstance(Retorno,Excepcion):
                    return Retorno
            gen.AddLabel(newLabel)
            return None
        return Excepcion("Semantico","Error no existe es tipo de dato"+str(condicion_v.tipo),self.fila,self.columna)

    def getNodo(self):
        nodo = NodoAST("IF")

        instruccionesIf = NodoAST("INSTRUCCIONES IF")
        for instr in self.instruccionesIf:
            instruccionesIf.agregarHijoNodo(instr.getNodo())
        nodo.agregarHijoNodo(instruccionesIf)

        if self.instruccionesElse != None:
            instruccionesElse = NodoAST("INSTRUCCIONES ELSE")
            for instr in self.instruccionesElse:
                instruccionesElse.agregarHijoNodo(instr.getNodo())
            nodo.agregarHijoNodo(instruccionesElse) 
        elif self.elseIf != None:
            nodo.agregarHijoNodo(self.elseIf.getNodo())

        return nodo