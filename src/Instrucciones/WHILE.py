from ..Abstract.abstract import Abstract
from ..Tabla_Simbolos.Exception import Exception
from ..Tabla_Simbolos.tabla_simbolos import TablaSimbolos
from ..Instrucciones.Break_Continue import Break
from ..Instrucciones.Break_Continue import Continue
from ..Instrucciones.Return import Return
from ..Abstract.Tipo import TIPO
from ..Tabla_Simbolos.generador import Generador

class While(Abstract):

    def __init__(self, condicion, instrucciones, fila, columna):
        self.condicion = condicion
        self.instrucciones = instrucciones
        super().__init__(fila, columna)

    def interpretar(self, arbol, tabla):
        gen = Generador()
        generator = gen.getInstance()
        generator.addComment("Compilando while")
        inicio = generator.newLabel()
        generator.putLabel(inicio)
        condicion = self.condicion.interpretar(arbol, tabla)  # True o False
        if isinstance(condicion, Exception): return condicion

        if condicion.getTipo() == TIPO.BOOLEAN:
            generator.putLabel(condicion.getTrueLbl())

            tabla.breakLbl = condicion.getFalseLbl()
            tabla.continueLbl = inicio

            nuevo_entorno = TablaSimbolos(tabla, "WHILE")
            nuevo_entorno.breakLbl = tabla.breakLbl  # seteando en caso de tener un ciclo mas arriba
            nuevo_entorno.continueLbl = tabla.continueLbl  # seteando en caso de tener un ciclo mas arriba
            nuevo_entorno.returnLbl = tabla.returnLbl  # seteando en caso de tener una funcion mas arriba

            for ins in self.instrucciones:
                value = ins.interpretar(arbol, nuevo_entorno)
                if isinstance(value, Exception): arbol.getErrores().append(value)
                if isinstance(value, Break):
                    generator.addGoto(condicion.getFalseLbl())
                if isinstance(value, Continue):
                    generator.addGoto(inicio)
                if isinstance(value, Return):
                    if nuevo_entorno.returnLbl != '':
                        if value.getTrueLbl() == '':
                            generator.addComment('Resultado a retornar en la funcion')
                            generator.setStack('P', value.getValor())
                            generator.addGoto(nuevo_entorno.returnLbl)
                            generator.addComment('Fin del resultado a retornar')
                        else:
                            generator.addComment('Resultado a retornar en la funcion')
                            generator.putLabel(value.getTrueLbl())
                            generator.setStack('P', '1')
                            generator.addGoto(nuevo_entorno.returnLbl)
                            generator.putLabel(value.getFalseLbl())
                            generator.setStack('P', '0')
                            generator.addGoto(nuevo_entorno.returnLbl)
                            generator.addComment('Fin del resultado a retornar')
                    else:
                        generator.addComment("Error: Sentencia return fuera de una funcion")
                        tm = Exception("Semantico", "Sentencia return fuera de una funcion", self.fila, self.columna)
                        arbol.getErrores.append(tm)
            tabla.breakLbl = ''
            tabla.continueLbl = ''

            generator.addGoto(inicio)
            generator.putLabel(condicion.getFalseLbl())
            generator.addComment("Finalizando While")
        else:
            generator.addComment("Error: la condicion debe ser de tipo boolean")
            return Exception("Semantico", "La condicional debe ser de tipo boolean", self.fila, self.columna)

        return None
