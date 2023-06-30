
import json
class Simbolo:
    
    def __init__(self, identificador, tipo,arreglo, fila, columna, posicion,tamano):
        self.id = identificador
        self.tipo = tipo
        self.arreglo = arreglo
        self.fila = fila
        self.columna = columna
        self.posicion = posicion
        self.tamano = tamano
        
    
        

    def getID(self):
        return self.id

    def setID(self, id):
        self.id = id

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo = tipo  

    def getPosicion(self):
        return self.posicion

    def setPosicion(self, posicion):
        self.posicion = posicion
    
    def getFila(self):
        return self.fila
    
    def getColumna(self):
        return self.columna
    
    def getArreglo(self):
        return self.arreglo
    
    def setTamano(self,tam):
        self.tamano = tam
    
    def getTamano(self):
        return self.tamano
    
    
    #para poder serializar en json
    def __json__(self):
        return self.__dict__