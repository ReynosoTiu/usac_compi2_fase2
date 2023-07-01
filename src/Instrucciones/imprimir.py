from ..Abstract.abstract import Abstract
from ..Tabla_Simbolos.Exception import Exception
from ..Tabla_Simbolos.generador import Generador
from ..Abstract.Tipo import TIPO

class Imprimir(Abstract):

    def __init__(self, expresion, fila, columna):
        self.expresion = expresion # <<Class.Primitivos>>
        super().__init__(fila, columna)
    
    def interpretar(self, tree, table):
        genAux = Generador()
        generator = genAux.getInstance()

        if self.expresion is not None :
            for val in self.expresion:
                value = val.interpretar(tree, table)
                if isinstance(value, Exception): return value  # Verifica si hubo un error en esa rama
                # print(value)

                if value.getTipo() == TIPO.NUMBER:
                    if isinstance(value.getValue(), int):
                        generator.addPrintNum2(value.getValue())
                    else:
                        generator.addPrintNum(value.getValue())
                elif value.getTipo() == TIPO.STRING:
                    generator.fPrintString()
                    paramTemp = generator.addTemp()
                    # print("Es la tabla completa en todos? ", table.size)
                    generator.addExp(paramTemp, 'P', table.size, '+')
                    generator.addExp(paramTemp, paramTemp, 1, '+')
                    generator.setStack(paramTemp, value.value)

                    generator.newEnv(table.size)
                    generator.callFun('printString')

                    temp = generator.addTemp()
                    # generator.getStack(temp, 'P')
                    generator.retEnv(table.size)
                elif value.getTipo() == TIPO.BOOLEAN:
                    tempLbl = generator.newLabel()
                    generator.putLabel(value.getTrueLbl())
                    generator.printTrue()
                    generator.addGoto(tempLbl)
                    generator.putLabel(value.getFalseLbl())
                    generator.printFalse()
                    generator.putLabel(tempLbl)

            generator.addPrintChar(10)
        else:
            return Exception("Semantico","La expresion no retorna un valor", self.fila, self.columna)