from Abstract.Instruccion import Instruccion
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO

class Imprimir(Instruccion):
    def __init__(self, expresion, fila, columna):
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table,gen):
        for expresion_ in self.expresion:
            temp_expresion = expresion_.interpretar(tree,table,gen)#Ejecuacion de las expresiones

            if isinstance(temp_expresion,Excepcion):
                return temp_expresion

            if temp_expresion.tipo == TIPO.NUMBER:
                gen.AddComment("====================    IMPRIMIENDO NUMERO  ====================")
                gen.AddPrintf("f", str(temp_expresion.valor))
                gen.AddPrintf("c", "10")
                gen.AddBr()
            elif temp_expresion.tipo == TIPO.STRING:
                gen.AddComment("====================    IMPRIMIENDO STRING  ====================")
                #llamar a generar printstring
                gen.GeneratePrintString()
                #agregar codigo en el main
                NewTemp1 = gen.newTemp()
                NewTemp2 = gen.newTemp()
                size = table.Size
                gen.AddExpression(NewTemp1, "P", str(size), "+")
                gen.AddComment("====================    ESPACIO RETORNO  ====================")
                gen.AddExpression(NewTemp1, NewTemp1, "1", "+")
                gen.AddComment("====================    STRING EN PARAMETRO  ====================")
                gen.AddSetStack("int("+ NewTemp1+")", temp_expresion.valor)
                gen.AddComment("====================    CAMBIO DE RETORNO   ====================")
                gen.AddExpression("P", "P", str(size), "+")
                gen.AddComment("====================    LLAMADA ====================")
                gen.AddCall("printString")
                gen.AddComment("====================    OBTENER RETORNO   ====================")
                gen.AddGetStack(NewTemp2, "int(P)")
                gen.AddComment("====================    REGRESO AL ENTORNO ====================")
                gen.AddExpression("P", "P", str(size), "-")
                gen.AddComment("salto de linea")
                gen.AddPrintf("c", "10")
                gen.AddBr()
            elif temp_expresion.tipo == TIPO.BOOLEAN:
                gen.AddComment("==================== IMPRIMIENDO BOOL ====================")
                newLabelSalida = gen.newLabel()
                newFalseLabel = gen.newLabel()
                
                if temp_expresion.isTemp:
                    gen.AddIf(temp_expresion.valor, "1", "!=", newFalseLabel)
                    for j in range(len(temp_expresion.TrueLvl)):
                        gen.AddGoto(temp_expresion.TrueLvl[j])
                        
                    for j in range(len(temp_expresion.FalseLvl)):
                        gen.AddGoto(temp_expresion.FalseLvl[j])
                    
                gen.AddGoto(newFalseLabel)  #Agregando etiqueta false sino F
                #add true labels
                
                for i in range(len(temp_expresion.TrueLvl)):
                    gen.AddLabel(temp_expresion.TrueLvl[i])
               
                gen.AddPrintf("c", "116")
                gen.AddPrintf("c", "114")
                gen.AddPrintf("c", "117")
                gen.AddPrintf("c", "101")
                gen.AddGoto(newLabelSalida)
                #add false labels
                
                for j in range(len(temp_expresion.FalseLvl)):
                    gen.AddLabel(temp_expresion.FalseLvl[j])
                
                gen.AddLabel(newFalseLabel)#->para no agregar etiqueta de mas
                gen.AddPrintf("c", "102")
                gen.AddPrintf("c", "97")
                gen.AddPrintf("c", "108")
                gen.AddPrintf("c", "115")
                gen.AddPrintf("c", "101")

                gen.AddLabel(newLabelSalida)
                gen.AddPrintf("c", "10")
                gen.AddBr()

    
    def getNodo(self):
        nodo = NodoAST("IMPRIMIR")
        for temp_expresion in self.expresion:
            nodo.agregarHijoNodo(temp_expresion.getNodo())
        return nodo