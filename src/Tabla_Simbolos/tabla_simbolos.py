from .Exception import Exception
from .simbolo import Simbolo
class TablaSimbolos:

    def __init__(self, anterior = None, name="Global"):
        self.tabla = {} # Al inicio la tabla esta vacia
        self.anterior = anterior # Apuntador al entorno anterior
        ### NUEVO PARA FASE 2 ###
        self.breakLbl = ''
        self.continueLbl = ''
        self.returnLbl = ''
        self.recTemps = False
        self.size = 0
        self.name = name
        self.tabla_reporte = []
        if anterior != None:
            self.size = self.anterior.size
            
    def getTablaG(self):
        return self.tabla
    
    def setTabla(self, id, tipo, inHeap, find = True):
        if id in self.tabla:
            self.tabla[id].setTipo(tipo)
            self.tabla[id].setInHeap(inHeap)
            return self.tabla[id]
        else:
            simbolo = Simbolo(id,tipo,self.size,self.anterior == None, inHeap)
            self.size += 1
            self.tabla[id] = simbolo
            itetm = {'id': simbolo.ide, 'type': simbolo.type, 'name': self.name, 'pos': simbolo.pos }
            temp = self
            ent = self
            while ent.anterior != None:
                ent = ent.anterior
            self.tabla_reporte.append(itetm)
            return temp.tabla[id]

    def setTablaFuncion(self, simbolo):
        self.tabla[simbolo.getID()] = simbolo
    
    def getTabla(self, ide): # Aqui manejamos los entornos :3
        tablaActual = self
        while tablaActual != None:
            if ide in tablaActual.tabla:
                return tablaActual.tabla[ide]
            else:
                tablaActual = tablaActual.anterior
        return None
    
    def updateTabla(self, simbolo):
        tablaActual = self
        while tablaActual != None:
            if simbolo.getID() in tablaActual.tabla:
                tablaActual.tabla[simbolo.getID()].setValor(simbolo.getValor())
                return None
                # Si necesitan cambiar el tipo de dato
                # tablaActual.tabla[simbolo.getID()].setTipo(simbolo.getTipo())
            else:
                tablaActual = tablaActual.anterior
        return Exception("Semantico", "Variable no encontrada.", simbolo.getFila(), simbolo.getColumna())

    def getTablaReporte(self):
        return self.tabla_reporte