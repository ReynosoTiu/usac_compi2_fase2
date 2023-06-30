class Arbol:
    def __init__(self, instrucciones ):
        self.instrucciones = instrucciones
        self.funciones = []
        self.excepciones = []
        self.tabla_reporte = []
        #self.tabla_reporte = []self.tabla_reporte = {}
        self.consola = ""
        self.TSglobal = None
        self.dot = ""
        self.contador = 0


    def getInstrucciones(self):
        return self.instrucciones

    def setInstrucciones(self, instrucciones):
        self.instrucciones = instrucciones

    def getExcepciones(self):
        return self.excepciones

    def setExcepciones(self, excepciones):
        self.excepciones = excepciones

    def getConsola(self):
        return self.consola
    
    def setConsola(self, consola):
        self.consola = consola

    def updateConsola(self,cadena):
        self.consola += '>>'+str(cadena) + '\n' #aqui se le agrego >> para la consola

    def getTSGlobal(self):
        return self.TSglobal
    
    def setTSglobal(self, TSglobal):
        self.TSglobal = TSglobal
    
    def getFunciones(self):
        return self.funciones

    def getFuncion(self, nombre):
        for funcion in self.funciones:
            if funcion.nombre == nombre:
                return funcion
        return None
    
    def addFuncion(self, funcion):
        self.funciones.append(funcion)
    
    def addSim_Tabla(self,agregarInf):
        encontrado = False
        for item in self.tabla_reporte:
            # ID == ID_rep       entorno == entorno_rep        fila == fila_rep
            if agregarInf[0] == item[0] and agregarInf[3] == item[3] and agregarInf[5] == item[5]:
                item[4] = agregarInf[4]
                encontrado = True
                break
        if not encontrado:
            self.tabla_reporte.append(agregarInf)
    
    def actualizarSim_Tabla_reporte(self,id,ts):
        #si la variable existe en el entorno
        while ts != None:
            if id in ts.tabla:
                simbolo_temp = ts.tabla[id]
                for item in self.tabla_reporte:
                    # id == id_ts  fila == fila_ts
                    if item[0] == simbolo_temp.id and item[5] == simbolo_temp.fila:
                        #print("valor simbolo", simbolo_temp.valor, item)
                        #print(item[4])
                        item[4] = simbolo_temp.valor
                        #print(item[4])
                        break
                break
            else:
                ts = ts.anterior

    
    def getSim_Tabla(self):
        return self.tabla_reporte

    def getDot(self, raiz): ## DEVUELVE EL STRING DE LA GRAFICA EN GRAPHVIZ
        self.dot = ""
        self.dot += "digraph {\n"
        self.dot +="rankdir=UD\n"# borrar por si acaso
        self.dot +="node[shape=record]\n" #borrar por si acaso
        self.dot += "n0[label=\"" + raiz.getValor().replace("\"", "\\\"") + "\"];\n"
        self.contador = 1
        self.recorrerAST("n0", raiz)
        self.dot += "}"
        return self.dot

    def recorrerAST(self, idPadre, nodoPadre):
        for hijo in nodoPadre.getHijos():
            nombreHijo = "n" + str(self.contador)
            self.dot += nombreHijo + "[label=\"" + hijo.getValor().replace("\"", "\\\"") + "\"];\n"
            self.dot += idPadre + "->" + nombreHijo + ";\n"
            self.contador += 1
            self.recorrerAST(nombreHijo, hijo)

    
    