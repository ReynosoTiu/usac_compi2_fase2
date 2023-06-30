from TS.Simbolo import Simbolo
from Instrucciones.Funcion import Funcion
from Abstract.Instruccion import Instruccion
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break
#____________________________________ FUNCIONES NATIVAS ____________________________
from Nativas.Truncate import Truncate


class Llamada(Instruccion):
    def __init__(self, nombre, parametros, fila, columna):
        self.nombre = nombre
        self.parametros = parametros
        self.fila = fila
        self.columna = columna
        self.arreglo = False
    
    def interpretar(self, tree, table,gen):
        result = tree.getFuncion(self.nombre) ## OBTENER LA FUNCION
        if result == None: # NO SE ENCONTRO LA FUNCION
            return Excepcion("Semantico", "NO SE ENCONTRO LA FUNCION: " + self.nombre, self.fila, self.columna)
        
        nuevaTabla = TablaSimbolos(tree.getTSGlobal(),"FUNCION "+result.nombre)
        # OBTENER PARAMETROS
        if len(result.parametros) == len(self.parametros): #LA CANTIDAD DE PARAMETROS ES LA ADECUADA
            contador=0

            
            for expresion in self.parametros: # SE OBTIENE EL VALOR DEL PARAMETRO EN LA LLAMADA
                
                resultExpresion = expresion.interpretar(tree, table)
                
                

                if isinstance(resultExpresion, Excepcion): return resultExpresion
                
                #________________trucate________________________________________
                if result.nombre == "truncate":
                    #creacion simbolo
                    simbolo = Simbolo(str(result.parametros[contador]['identificador']),expresion.tipo,False, self.fila, self.columna, resultExpresion)
                    resultTabla = nuevaTabla.setTabla(simbolo)
                    if isinstance(resultTabla, Excepcion): 
                        return resultTabla
                    break
                #_________________round____________________________________________
                if result.nombre == "round":
                    #creacion simbolo
                    simbolo = Simbolo(str(result.parametros[contador]['identificador']),expresion.tipo,False,self.fila, self.columna, resultExpresion)
                    resultTabla = nuevaTabla.setTabla(simbolo)
                    if isinstance(resultTabla, Excepcion): 
                        return resultTabla
                    break
                
                #_________________typeof____________________________________________
                if result.nombre == "typeof":
                    #creacion simbolo
                    simbolo = Simbolo(str(result.parametros[contador]['identificador']),expresion.tipo,False,self.fila, self.columna, resultExpresion)
                    resultTabla = nuevaTabla.setTabla(simbolo)
                    if isinstance(resultTabla, Excepcion): 
                        return resultTabla
                    break
                #_________________ length ____________________________________________
                if result.nombre == "length":
                    #creacion simbolo
                    simbolo = Simbolo(str(result.parametros[contador]['identificador']),expresion.tipo,expresion.arreglo,self.fila, self.columna, resultExpresion)
                    resultTabla = nuevaTabla.setTabla(simbolo)
                    if isinstance(resultTabla, Excepcion): 
                        return resultTabla
                    break


                if result.parametros[contador]["tipo"] == expresion.tipo:  # VERIFICACION DE TIPO
                    # CREACION DE SIMBOLO E INGRESARLO A LA TABLA DE SIMBOLOS
                    
                    simbolo = Simbolo(str(result.parametros[contador]['identificador']), result.parametros[contador]['tipo'],expresion.arreglo, self.fila, self.columna, resultExpresion)
                    resultTabla = nuevaTabla.setTabla(simbolo)
                    if isinstance(resultTabla, Excepcion): return resultTabla

                else:
                    return Excepcion("Semantico", "Tipo de dato diferente en Parametros de la llamada.", self.fila, self.columna)
                contador += 1

            
        else: 
            return Excepcion("Semantico", "Cantidad de Parametros incorrecta.", self.fila, self.columna)
        
        
        value = result.interpretar(tree, nuevaTabla,gen)         # INTERPRETAR EL NODO FUNCION
        
        if isinstance(value, Excepcion): 
            return value
        
        #if self.tipo != result.tipo:
        #    return Excepcion("Semantico", "Tipo de dato diferente en retorno"+str(self.tipo)+" != "+str(result.tipo), self.fila, self.columna)
            
        self.tipo = result.tipo
        gen.AddComment("==================   CAMBIO DE ENTORNO   ==================")
        gen.AddExpression("P","P",str(table.Size),"+")
        gen.AddCall(result.nombre)
        gen.AddComment("==================   REGRESO A ENTORNO   ==================")
        gen.AddExpression("P","P",str(table.Size),"-")
        
        return value
    
    def getNodo(self):
        nodo = NodoAST("LLAMADA A FUNCION")
        nodo.agregarHijo(str(self.nombre))
        parametros = NodoAST("PARAMETROS")
        for param in self.parametros:
            parametros.agregarHijoNodo(param.getNodo())
        nodo.agregarHijoNodo(parametros)
        return nodo