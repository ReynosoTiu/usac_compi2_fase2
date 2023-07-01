from ..Tabla_Simbolos.Exception import Exception
from ..Abstract.abstract import Abstract
from ..Tabla_Simbolos.generador import Generador
from ..Abstract.auxiliar import Auxiliar
from ..Abstract.Tipo import TIPO
class Identificador(Abstract):
    def __init__(self, ide, atributo, fila, columna, tipo = None):
        self.ide = ide
        self.atributo = atributo
        self.tipo = tipo
        super().__init__(fila, columna)

    def interpretar(self, arbol, tabla):
        genAux = Generador()
        generator = genAux.getInstance()

        if self.atributo == None:
            generator.addComment("Acceso a variable")
            simbolo = tabla.getTabla(self.ide)
            if simbolo == None:
                generator.addComment("Fin de compilacion. Variable no encontrada")
                return Exception("Semantico", "Variable \""+self.ide+"\" no encontrada", self.fila, self.columna)
            temp = generator.addTemp()
            #self.tipo = simbolo.getTipo()
            # Obtencion de posicion de la variable
            tempPos = simbolo.pos
            if not simbolo.isGlobal:
                tempPos = generator.addTemp()
                generator.addExp(tempPos, 'P', simbolo.pos, '+')

            generator.getStack(temp, tempPos)
            if simbolo.type != TIPO.BOOLEAN:
                generator.addComment("Fin de compilacion de Acceso")
                generator.addSpace()
                self.tipo = simbolo.type
                return Auxiliar(temp, simbolo.type, True)

            if self.trueLbl == '':
                self.trueLbl = generator.newLabel()
            if self.falseLbl == '':
                self.falseLbl = generator.newLabel()

            generator.addIf(temp, '1', '==', self.trueLbl)
            generator.addGoto(self.falseLbl)

            generator.addComment("Fin de compilacion de Acceso")
            generator.addSpace()

            ret = Auxiliar(None, TIPO.BOOLEAN, True)
            ret.setTrueLbl(self.trueLbl)
            ret.setFalseLbl(self.falseLbl)
            self.tipo = simbolo.type
            return ret

        else:
            print("-ACCS--")
            generator.addComment("Acceso a variable struct")
            # verificar si el identificador existe en la tabla de simbolos
            struct = tabla.getTabla(self.ide)
            if struct is None:
                generator.addComment("Fin de compilacion. Variable no encontrada")
                return Exception("Semantico", "La variable \"" + self.ide + "\" no ha sido declarada", self.fila,
                             self.columna)

            # verificar si el simbolo es un struct
            if struct.getTipo() != 'STRUCT':
                generator.addComment("Fin de compilacion. Variable no es de tipo struct")
                return Exception("Semantico", "La variable \"" + self.ide + "\" no es de tipo struct", self.fila,
                             self.columna)
            # obteniendo entorno de atributos del struct
            entorno = struct.getInHeap()

            # verificando si el atributo existe
            atributo = entorno.getTabla(self.atributo)
            if atributo is None:
                generator.addComment("Fin de compilacion. El atributo no existe en la interface")
                return Exception("Semantico", "El atributo \"" + self.atributo + "\" no ha sido declarada", self.fila,self.columna)

            Ident = Identificador(self.atributo, None, self.fila, self.columna)
            tem_ident = Ident.interpretar(arbol, entorno)
            if isinstance(tem_ident, Exception): return tem_ident
            struct.inHeap = entorno
            generator.addComment("Finalizando Acceso a variable struct")
            return  tem_ident


    def getTipo(self):
        return self.tipo
    
    def getID(self):
        return self.ide