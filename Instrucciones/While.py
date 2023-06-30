from Abstract.Instruccion import Instruccion
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break
from Instrucciones.Continue import Continue
from Instrucciones.Return import Return

class While(Instruccion):
    def __init__(self, condicion, instrucciones, fila, columna):
        self.condicion = condicion
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table,gen):
        gen.AddComment("====================   GENERANDO WHILE ====================")
        #tiqueta de retorno
        RetLvl = gen.newLabel()
        gen.AddLabel(RetLvl)
        #ejecutando expresion
        condicion = self.condicion.interpretar(tree,table,gen)
        #aqui se agregarian etiquetas break y continue
        #agregando etiquetas verdaderas
        for i in range(len(condicion.TrueLvl)):
            gen.AddLabel(condicion.TrueLvl[i])
        #ejecutando instrucciones
        tablaWHile = TablaSimbolos(table,"WHILE")
        for instruccion in self.instrucciones:
            instruccion.interpretar(tree,tablaWHile,gen)
            #retorno
        gen.AddGoto(RetLvl)
        #agregando etiquetas falsas
        for i in range(len(condicion.FalseLvl)):
            gen.AddLabel(condicion.FalseLvl[i])
        # while True:
        #     condicion = self.condicion.interpretar(tree, table)
        #     if isinstance(condicion, Excepcion): return condicion

        #     if self.condicion.tipo == TIPO.BOOLEAN:
        #         if bool(condicion) == True:   # VERIFICA SI ES VERDADERA LA CONDICION
        #             nuevaTabla = TablaSimbolos(table,"WHILE")       #NUEVO ENTORNO
        #             for instruccion in self.instrucciones:
                        
        #                 result = instruccion.interpretar(tree, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL IF
        #                 if isinstance(result, Excepcion) :
        #                     tree.getExcepciones().append(result)
        #                     tree.updateConsola(result.toString())
                            
        #                 if isinstance(result, Break): 
        #                     return None
        #                 if isinstance(result,Continue):
        #                     break
        #                 if isinstance(result,Return):
        #                     return result
        #         else:
        #             break
        #     else:
        #         return Excepcion("Semantico", "Tipo de dato no booleano en IF.", self.fila, self.columna)
    
    def getNodo(self):
        nodo = NodoAST("WHILE")

        instrucciones = NodoAST("INSTRUCCIONES")
        for instr in self.instrucciones:
            instrucciones.agregarHijoNodo(instr.getNodo())
        nodo.agregarHijoNodo(instrucciones)
        return nodo