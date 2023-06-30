#Libreria para convertir imagen en base64
import base64

#Aqui empieza todos los imports
from gramatica import parse,getErrores
import os
#import os
from Abstract.NodoAST import NodoAST
from Abstract.Generador import Generador
import webbrowser


pathFile=''
nombreFile=''
pathImagen = ''
ast = None 
generadorC3D = None       
#__________________ Tabla ________________________________
from TS.Arbol import Arbol
from TS.TablaSimbolos import TablaSimbolos
from TS.Excepcion import Excepcion
#________________importanto instrucciones _________________
#from Instrucciones.Imprimir import Imprimir
from Instrucciones.Declaracion import Declaracion
from Instrucciones.Declaracion_sinAsignacion import Declaracion_sinAsignacion
from Instrucciones.Asignacion import Asignacion
#from Instrucciones.If import If
from Instrucciones.Break import Break
#from Instrucciones.While import While
#from Instrucciones.Incremento import Incremento
#from Instrucciones.For import For
#from Instrucciones.Switch import Switch
#from Instrucciones.Caso import Caso
#from Instrucciones.Continue import Continue
#from Instrucciones.Main import Main
from Instrucciones.Funcion import Funcion
from Instrucciones.Return import Return
from Instrucciones.ModificarArreglo import ModificarArreglo
from Instrucciones.DeclaracionArreglo import DeclaracionArreglo
from Instrucciones.DeclaracionArreglo2 import DeclaracionArreglo2
#_______________________ FUNCIONES NATIVAS ______________________________________
from Nativas.ToUpper import ToUpper
from Nativas.ToLower import ToLower
from Nativas.ToFixed import ToFixed
from Nativas.Truncate import Truncate
from Nativas.Round import Round
from Nativas.TypeOf import TypeOf
from Nativas.Length import Length 
#__________________________________ TS ___________________________________________
from TS.Tipo import TIPO
#___________________________________ REPORTE ______________________________________
from Reporte.Reporte import reporte
#___________________________________ READ _______________________________________
from Expresiones.AccesoArreglo import AccesoArreglo

def crearNativas(ast):
    #toUpper
    nombre = "toUpperCase"
    parametros = [{'tipo':TIPO.STRING,'identificador':'toUpperCase##Param1'}]
    instrucciones = []
    toUpper = ToUpper(nombre, parametros, instrucciones, -1, -1)
    ast.addFuncion(toUpper)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)

    #toLower
    nombre = "toLowerCase"
    parametros = [{'tipo':TIPO.STRING,'identificador':'toLowerCase##Param1'}]
    instrucciones = []
    toLower = ToLower(nombre, parametros, instrucciones, -1, -1)
    ast.addFuncion(toLower)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)
    
    #toFixed
    nombre = "toFixed"
    parametros = [{'tipo':TIPO.NUMBER,'identificador':'toFixed##Param1'}]
    instrucciones = []
    toFixed = ToFixed(nombre, parametros, instrucciones, -1, -1)
    ast.addFuncion(toFixed)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)

    #truncate 
    nombre = "Truncate"
    parametros = [{'tipo':TIPO.NUMBER,'identificador':'toTruncate##Param1'}]#si queres otro paramteo solo agregar , y otra lista
    instrucciones = []
    truncate = Truncate(nombre, parametros, instrucciones, -1, -1)
    ast.addFuncion(truncate)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)

    #Round
    nombre = "Round"
    parametros = [{'tipo':TIPO.NUMBER,'identificador':'toRound##Param1'}]#si queres otro paramteo solo agregar , y otra lista
    instrucciones = []
    roundd = Round(nombre, parametros, instrucciones, -1, -1)
    ast.addFuncion(roundd)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)

    #typeof
    nombre = "TypeOf"
    parametros_t = [{'tipo':TIPO.ANY,'identificador':'typeof##Param1'}]#si queres otro paramteo solo agregar , y otra lista
    instrucciones_t = []
    typeOf = TypeOf(nombre, parametros_t, instrucciones_t, -1, -1)
    ast.addFuncion(typeOf)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)

    #length
    nombre = "Length"
    parametros = [{'tipo':TIPO.ANY,'identificador':'length##Param1'}]
    instrucciones = []
    length = Length(nombre, parametros, instrucciones, -1, -1)
    ast.addFuncion(length)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)



def ejecutar_entrada(cont):
    instrucciones = parse(cont) # ARBOL AST
    
    global ast 
    global generadorC3D
    global pathImagen
    global nombreFile

    ast = Arbol(instrucciones)
    generadorC3D = Generador()
    generadorC3D.MainCode = True
    TSGlobal = TablaSimbolos(None,"Global")
    ast.setTSglobal(TSGlobal)
    crearNativas(ast)
    
    for error in getErrores():                   # CAPTURA DE ERRORES LEXICOS Y SINTACTICOS
        ast.getExcepciones().append(error)

    for instruccion in ast.getInstrucciones():      # 1ERA PASADA (DECLARACIONES Y ASIGNACIONES)
        
        if isinstance(instruccion, Funcion):
            ast.addFuncion(instruccion)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)
            ast.addSim_Tabla([instruccion.nombre,"Funcion","----","Global",'----',instruccion.fila,instruccion.columna])
        # if isinstance(instruccion, Declaracion) or isinstance(instruccion, Asignacion) or isinstance(instruccion,Declaracion_sinAsignacion) or isinstance(instruccion,DeclaracionArreglo) or isinstance(instruccion,ModificarArreglo) or isinstance(instruccion,AccesoArreglo) or isinstance(instruccion,DeclaracionArreglo2):

        #     value = instruccion.interpretar(ast,TSGlobal)
        #     if isinstance(value, Excepcion) :
        #         ast.getExcepciones().append([value.tipo,value.descripcion,value.fila,value.columna])
                
        #     if isinstance(value, Break): 
        #         err = Excepcion("Semantico", "Sentencia BREAK fuera de ciclo", instruccion.fila, instruccion.columna)
        #         ast.getExcepciones().append([err.tipo,err.descripcion,err.fila,err.columna])
                    
    for instruccion in ast.getInstrucciones():      # Ejecutar instrucciones
        if not (isinstance(instruccion, Funcion) ) :
            #or isinstance(instruccion, Declaracion) or isinstance(instruccion, Asignacion) or isinstance(instruccion,DeclaracionArreglo2) or isinstance(instruccion,DeclaracionArreglo) or isinstance(instruccion,ModificarArreglo) or isinstance(instruccion,AccesoArreglo)
            value = instruccion.interpretar(ast,TSGlobal,generadorC3D)
                
            if isinstance(value, Excepcion) :
                ast.getExcepciones().append([value.tipo,value.descripcion,value.fila,value.columna])
                
            if isinstance(value, Break): 
                err = Excepcion("Semantico", "Sentencia BREAK fuera de ciclo", instruccion.fila, instruccion.columna)
                ast.getExcepciones().append([err.tipo,err.descripcion,err.fila,err.columna])
                
            if isinstance(value,Return):
                err = Excepcion("Semantico", "Sentencia Return fuera de funcion o ciclo", instruccion.fila, instruccion.columna)
                ast.getExcepciones().append([err.tipo,err.descripcion,err.fila,err.columna])
                
    generadorC3D.GenerateFinalCode()
    init = NodoAST("RAIZ")
    instr = NodoAST("INSTRUCCIONES")

    for instruccion in ast.getInstrucciones():
        instr.agregarHijoNodo(instruccion.getNodo())

    init.agregarHijoNodo(instr)
    grafo = ast.getDot(init) #DEVUELVE EL CODIGO GRAPHVIZ DEL AST

    dirname = os.path.dirname(__file__)
    nombreFile  = 'ast'
    direcc = os.path.join(dirname, nombreFile+'.dot')
    arch = open(direcc, "w+")
    arch.write(grafo)
    arch.close()
    #os.system('dot -T pdf -o '+nombreFile+'.pdf '+ nombreFile+'.dot')
    pathImagen = dirname+"/"+nombreFile+".png" 
    os.system('dot -T png -o '+nombreFile+'.png '+ nombreFile+'.dot')
    #Retorno consola
    return generadorC3D.FinalCode


def ast_grafica():
    global pathImagen
    print(pathImagen)
    with open(pathImagen, "rb") as archivo_imagen:
        imagen_codificada = base64.b64encode(archivo_imagen.read())
        return imagen_codificada.decode('utf-8')
    
def rep_errores():
    return ast.getExcepciones()

def rep_tabla_simbolo():
    return ast.getSim_Tabla()
    

