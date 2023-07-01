from ..Abstract.abstract import Abstract
from ..Tabla_Simbolos.generador import Generador
from ..Abstract.Tipo import TIPO
from ..Abstract.auxiliar import Auxiliar

class Primitivos(Abstract):

    def __init__(self, tipo, valor, fila, columna):
        self.tipo = tipo # Number, String, Boolean
        self.valor = valor # 4, 'hola', true

        # self.tipoAux = ''
        super().__init__(fila, columna)
    
    def interpretar(self, tree, table):
        # generando instancia
        genAux = Generador()
        generador = genAux.getInstance()
        # verificando si es de tipo any
        isTypeAny = self.tipo == TIPO.ANY

        if self.tipo == TIPO.NUMBER:
            return Auxiliar(self.valor, self.tipo, True)
        elif self.tipo == TIPO.STRING or isTypeAny:
            temporal = generador.addTemp()
            generador.addAsig(temporal, 'H')
            for char in str(self.valor):
                generador.setHeap2('H',ord(char)) # setear un valor en heap
                generador.nextHeap() # sumar un 1 al heap
            generador.setHeap('H',-1) # simular un fin de cadena con -1
            generador.nextHeap()
            if isTypeAny:
                temp = Auxiliar(temporal, TIPO.STRING, True, self.tipo)
                temp.auxType = TIPO.ANY
                return temp
            return Auxiliar(temporal, self.tipo, True)
        elif self.tipo == TIPO.BOOLEAN:
            if self.trueLbl == '':
                self.trueLbl = generador.newLabel()
            if self.falseLbl == '':
                self.falseLbl = generador.newLabel()

            if self.valor:
                generador.addGoto(self.trueLbl)
                generador.addComment("GOTO PARA EVITAR ERROR DE GO")
                generador.addGoto(self.falseLbl)
            else:
                generador.addGoto(self.falseLbl)
                generador.addComment("GOTO PARA EVITAR ERROR DE GO")
                generador.addGoto(self.trueLbl)

            ret = Auxiliar(self.valor, self.tipo, False)
            ret.trueLbl = self.trueLbl
            ret.falseLbl = self.falseLbl
            return ret


    def getTipo(self):
        return self.tipo
