from ..Tabla_Simbolos.Exception import Exception
from ..Abstract.abstract import Abstract
from ..Tabla_Simbolos.simbolo import Simbolo
from ..Abstract.Tipo import TIPO
from ..Tabla_Simbolos.generador import Generador
from ..Abstract.auxiliar import Auxiliar

class Declaracion(Abstract):

    def __init__(self, ide, tipo, valor, fila, columna):
        self.ide = ide # a
        self.tipo = tipo # Number, String, Boolean
        self.valor = valor # 4, 'hola', true
        self.find = True
        self.ghost = -1
        super().__init__(fila, columna)
    
    def interpretar(self, arbol, tabla):
        genAux = Generador()
        generator = genAux.getInstance()
        generator.addComment('Declarando variable')
        value = self.valor.interpretar(arbol, tabla)
        if isinstance(value, Exception): return value
        # Verificacion de tipos
        if self.tipo == TIPO.ANY:
            inHeap = value.getTipoAux() == TIPO.STRING
            simbolo = tabla.setTabla(self.ide, value.getTipo(), inHeap, self.find)
            simbolo.tipoAux = self.tipo
        elif str(self.tipo) == str(value.getTipo()):
            inHeap = value.getTipo() == TIPO.STRING
            simbolo = tabla.setTabla(self.ide, value.getTipo(), inHeap, self.find)
            arbol.tabla_reporte.append([simbolo.ide,str(simbolo.type),simbolo.pos])
        else:
            generator.addComment('Error, tipo de dato diferente declarado.')
            result = Exception("Semantico", "Tipo de dato diferente declarado.", self.fila, self.columna)
            return result

        tempPos = simbolo.pos
        if not simbolo.isGlobal:
            tempPos = generator.addTemp()
            generator.addExp(tempPos, 'P', simbolo.pos, '+')

        if value.getTipo() == TIPO.BOOLEAN:
            tempLbl = generator.newLabel()
            generator.putLabel(value.trueLbl)
            generator.setStack(tempPos, "1")
            generator.addGoto(tempLbl)
            generator.putLabel(value.falseLbl)
            generator.setStack(tempPos, "0")
            generator.putLabel(tempLbl)
           # arbol.tabla_reporte.append([simbolo.ide,str(simbolo.type),simbolo.pos])
            #arbol.tabla_reporte.append({'id': simbolo.ide, 'type': simbolo.type, 'name': self.name, 'pos': simbolo.pos })
        else:
            generator.setStack(tempPos, value.value)
        generator.addComment('Finalizando declaracion de variable')