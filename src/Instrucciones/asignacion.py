from ..Abstract.abstract import Abstract
from ..Tabla_Simbolos.Exception import Exception
from ..Abstract.Tipo import TIPO
from ..Tabla_Simbolos.generador import Generador
from ..Abstract.auxiliar import Auxiliar


class Asignacion(Abstract):
    def __init__(self, identificador, expresion, fila, columna):
        self.identificador = identificador
        self.expresion = expresion
        super().__init__(fila, columna)

    def interpretar(self, tree, table):
        genAux = Generador()
        generator = genAux.getInstance()
        generator.addComment('Reasignando valor a variable')

        valor = self.expresion.interpretar(tree, table)
        if isinstance(valor, Exception): return valor  # Verifica si hubo un error en esa rama
        simbolo = table.getTabla(self.identificador)
        # Verificacion de tipos
        if simbolo == None:
            generator.addComment("No se encontro la variable")
            return Exception("Semantico", "Variable \""+self.identificador+"\" no encontrada", self.fila, self.columna)
        # tipo_string = (simbolo.getTipo() and valor.type == TIPO.STRING)
        # tipo_number = (simbolo.getTipo() and valor.type == TIPO.NUMBER)
        # tipo_bool = (simbolo.getTipo() and valor.type == TIPO.BOOLEAN)
        # if tipo_bool or tipo_string or tipo_number or simbolo.getTipoAux() == TIPO.ANY:
        if simbolo.getTipo() == valor.type:
            generator.setStack(simbolo.getPos(), valor.value)
            generator.addComment('Finalizando reasignando de variable')
            return None
        elif simbolo.getTipoAux() == TIPO.ANY:
            simbolo.type = valor.type # seteando el tipo de la expresion a variable typo any
            generator.setStack(simbolo.getPos(), valor.value)
            generator.addComment('Finalizando reasignando de variable')
            return None
        else:
            generator.addComment("No coinciden los tipos de datos")
            result = Exception("Semantico", "No coinciden los tipos de datos en la variable: \""+self.identificador+"\".", self.fila, self.columna)
            return result
