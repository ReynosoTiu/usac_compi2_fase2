from ..Abstract.abstract import Abstract
from ..Tabla_Simbolos.Exception import Exception
from ..Instrucciones.Break_Continue import Break
from ..Instrucciones.Break_Continue import Continue
from ..Tabla_Simbolos.tabla_simbolos import TablaSimbolos
from ..Instrucciones.Return import Return
from ..Abstract.Tipo import TIPO
from ..Tabla_Simbolos.simbolo import Simbolo
from ..Tabla_Simbolos.generador import Generador
class For(Abstract):
    def __init__(self, row, column, declaration, condition, incrdecr, instructions):
        self.inicio = declaration
        self.condicion = condition
        self.aumento = incrdecr
        self.bloqueFor = instructions
        super().__init__(row, column)

    def interpretar(self, arbol,tabla):
        genAux = Generador()
        generador = genAux.getInstance()
        generador.addComment("Compilando for")

        nuevo_entorno = TablaSimbolos(tabla, "FOR")

        declaracion = self.inicio.interpretar(arbol, nuevo_entorno)
        if isinstance(declaracion, Exception): return declaracion

        inicio = generador.newLabel()
        generador.putLabel(inicio)

        condicion = self.condicion.interpretar(arbol, nuevo_entorno)  # True o False
        if isinstance(condicion, Exception): return condicion

        if condicion.getTipo() == TIPO.BOOLEAN:
            generador.putLabel(condicion.getTrueLbl())

            tabla.breakLbl = condicion.getFalseLbl()
            tabla.continueLbl = inicio

            nuevo_entorno.breakLbl = tabla.breakLbl  # seteando en caso de tener un ciclo mas arriba
            nuevo_entorno.continueLbl = tabla.continueLbl  # seteando en caso de tener un ciclo mas arriba
            nuevo_entorno.returnLbl = tabla.returnLbl  # seteando en caso de tener una funcion mas arriba

            for ins in self.bloqueFor:
                #nuevo_entorno = TablaSimbolos(tabla)
                value = ins.interpretar(arbol, nuevo_entorno)
                if isinstance(value, Exception): arbol.getErrores().append(value)
                if isinstance(value, Break):
                    generador.addGoto(condicion.getFalseLbl())
                if isinstance(value, Continue):
                    generador.addGoto(inicio)
                if isinstance(value, Return):
                    if nuevo_entorno.returnLbl != '':
                        if value.getTrueLbl() == '':
                            generador.addComment('Resultado a retornar en la funcion')
                            generador.setStack('P', value.getValor())
                            generador.addGoto(nuevo_entorno.returnLbl)
                            generador.addComment('Fin del resultado a retornar')
                        else:
                            generador.addComment('Resultado a retornar en la funcion')
                            generador.putLabel(value.getTrueLbl())
                            generador.setStack('P', '1')
                            generador.addGoto(nuevo_entorno.returnLbl)
                            generador.putLabel(value.getFalseLbl())
                            generador.setStack('P', '0')
                            generador.addGoto(nuevo_entorno.returnLbl)
                            generador.addComment('Fin del resultado a retornar')
                    else:
                        generador.addComment("Error: Sentencia return fuera de una funcion")
                        tm = Exception("Semantico", "Sentencia return fuera de una funcion", self.fila, self.columna)
                        arbol.getErrores.append(tm)

            incremento = self.aumento.interpretar(arbol, nuevo_entorno)
            if isinstance(incremento, Exception): return incremento

            tabla.breakLbl = ''
            tabla.continueLbl = ''

            generador.addGoto(inicio)
            generador.putLabel(condicion.getFalseLbl())
            generador.addComment("Finalizando For")
        else:
            generador.addComment("Error: la condicion debe ser de tipo boolean")
            return Exception("Semantico", "La condicional debe ser de tipo boolean", self.fila, self.columna)

        return None