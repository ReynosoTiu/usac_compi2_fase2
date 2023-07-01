from ..Abstract.abstract import Abstract
from ..Tabla_Simbolos.Exception import Exception
from ..Abstract.Tipo import NATIVA
from ..Abstract.Tipo import TIPO
from ..Tabla_Simbolos.generador import Generador
from ..Abstract.auxiliar import Auxiliar


class Nativas(Abstract):

    def __init__(self, identificador, tipo, expresion, fila, columna):
        self.identificador = identificador
        self.tipo = tipo
        self.expresion = expresion
        super().__init__(fila, columna)

    def interpretar(self, arbol, tabla):
        # creando instancia
        genAux = Generador()
        generator = genAux.getInstance()
        if self.identificador is None and self.tipo == NATIVA.TYPEOF:
            generator.addComment("--NATIVAS--")
            var = self.expresion.interpretar(arbol, tabla)
            if isinstance(var, Exception):
                generator.addComment("--NO SE ENCONTRO LA VARIABLE--")
                return var
            if var.getTipo() == TIPO.BOOLEAN:
                generator.putLabel(var.getTrueLbl())
                generator.putLabel(var.getFalseLbl())
            # obteniendo el valor string del tipo enum
            tipo = var.getTipo().name
            # generando temporal donde estara el indice del tipo
            temporal = generator.addTemp()
            generator.addAsig(temporal, 'H')
            # recorriendo cadena del tipo
            for val in tipo:
                generator.setHeap2('H', ord(val))  # setear un valor en heap
                generator.nextHeap()  # sumar un 1 al heap
            generator.setHeap('H', -1)  # simular un fin de cadena con -1
            generator.nextHeap()
            return Auxiliar(temporal, TIPO.STRING, True)

        # verifica si el identificador existe
        variable = self.identificador.interpretar(arbol, tabla)
        if isinstance(variable, Exception):
            generator.addComment("--NO SE ENCONTRO LA VARIABLE--")
            return id
        generator.addComment("------NATIVAS-------")
        # verifica si no hay errores en la expresion parametro
        parametro = self.expresion
        if parametro != None:
            parametro = self.expresion.interpretar(arbol, tabla)
        if isinstance(parametro, Exception): return parametro  # Verifica si hubo un Exception en esa rama

        # verifica el tipo de dato de la variable
        if variable.getTipo() == TIPO.NUMBER:
            if (self.tipo == NATIVA.APROXIMACION) and parametro.getTipo() == TIPO.NUMBER:
                # ingresa solo si la funcion es toFixed y el parametro es de tipo entero
                temporal = generator.addTemp()
                generator.addFixed(temporal, variable.getValue(), parametro.getValue())
                return Auxiliar(temporal, TIPO.NUMBER, True)
            elif (self.tipo == NATIVA.EXPONENCIAL) and (parametro.getTipo() == TIPO.NUMBER):
                # ingresa solo si la funcion es toExponential y el parametro es de tipo entero
                temporal = generator.addTemp()
                generator.addExponential(temporal, variable.getValue())
                return Auxiliar(temporal, TIPO.STRING, True)
            elif self.tipo == NATIVA.STRING:
                # ingresa solo si la funcion es toString
                temporal = generator.addTemp()
                generator.addtoString(temporal, variable.getValue())
                return Auxiliar(temporal, TIPO.STRING, True)
            else:
                generator.addComment("El tipo de parametro o variable no coincide para la funcion")
                return Exception("Semantico", "El tipo de parametro o variable no coincide para la funcion", self.fila, self.columna)

        elif variable.getTipo() == TIPO.STRING:
            # el id de la variable es tipo string
            if self.tipo == NATIVA.UPPER :
                temporal = generator.addTemp()
                generator.addUpper(temporal,variable.getValue())
                return Auxiliar(temporal, TIPO.STRING, True)
            elif self.tipo == NATIVA.STRING:
                # ingresa solo si la funcion es toString
                return Auxiliar(variable.getValue(), TIPO.STRING, True)
            elif self.tipo == NATIVA.LOWER :
                temporal = generator.addTemp()
                generator.addLower(temporal, variable.getValue())
                return Auxiliar(temporal, TIPO.STRING, True)
            elif self.tipo == NATIVA.SPLIT:
                if isinstance(parametro, str):
                    # el parametro es correcto - de tipo string
                    # crear clase arreglo e ingresar los valores y posiblemente retornar el valor interpretado
                    return variable.getValor().split(parametro)
                else:
                    return Exception("Semantico", "El tipo de parametro no coincide para la funcion", self.fila,self.columna)
            else:
                return Exception("Semantico", "El tipo de variable no coincide para la funcion", self.fila, self.columna)
