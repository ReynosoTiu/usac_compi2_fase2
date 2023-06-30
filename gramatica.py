''' 
------------------------------
JOSE CASTRO SINCU       201504115
JOSE LUIS REYNOSO TIU   201345126
VACACIONES DE JUNIO 2023
ORGANIZACION DE LENGUAJES Y COMPILADORES 2
-------------------------------
'''
import re
from TS.Excepcion import Excepcion
import sys

sys.setrecursionlimit(3000)
#______________________________________ LEXICO ___________________________
errores = []
reservadas = {
    'number'   : 'Rnumber',
    'boolean':'Rboolean',
    'string': 'Rstring',
    'any':'Rany',
    'void':'Rvoid',
    'let':'Rlet',
    'if':'Rif',
    'else':'Relse',
    'console' : 'Rconsole',
    'log' : 'Rlog',
    'break' : 'Rbreak',
    'while' : 'Rwhile',
    'for'   : 'Rfor',
    'switch' : 'Rswitch',
    'case' : 'Rcase',
    'default' : 'Rdefault',
    'continue' : 'Rcontinue',
    'Null' : 'Rnull',
    'main' : 'Rmain',
    'function' : 'Rfunc',
    'return': 'Rreturn',
    'read' : 'Rread',
    'true' : 'Rtrue',
    'false': 'Rfalse',
    'new' :'Rnew',
    'toFixed' :'RtoFixed',
    'toExponential' : 'RtoExponential',
    'toString' : 'RtoString',
    'toLowerCase' : 'RtoLowerCase',
    'toUpperCase' : 'RtoUpperCase',
    'length' : 'Rlength',
    'split' : 'Rsplit'
}

tokens  = [
    'PUNTOCOMA',
    'PARA',
    'PARC',
    'LLAVEA',
    'LLAVEC',
    'COMA',
    'MAS',
    'MENOS',
    'POR',
    'DIV',
    'POT',
    'MOD',
    'MENORIGUAL',
    'MENOR',
    'MAYORIGUAL',
    'MAYOR',
    'IGUALIGUAL',
    'DISTINTO',
    'AND',
    'OR',
    'NOT',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'IGUAL',
    'CARACTER',
    'ID',
    'MASMAS',
    'MENOSMENOS',
    'DOSPUNTO',
    'CORA',
    'CORC',
    'PUNTO'
] + list(reservadas.values())

# Tokens
t_PUNTOCOMA     = r';'
t_PARA          = r'\('
t_PARC          = r'\)'
t_LLAVEA        = r'{'
t_LLAVEC        = r'}'
t_MAS           = r'\+'
t_MENOS         = r'-'
t_POR           = r'\*'
t_DIV           = r'/'
t_POT           = r'\*\*'
t_MOD           = r'%'
t_MENOR         = r'<'
t_MENORIGUAL    = r'<='
t_MAYOR         = r'>'
t_MAYORIGUAL    = r'>='
t_IGUALIGUAL    = r'==='
t_DISTINTO      = r'!=='
t_AND           = r'&&'
t_OR            = r'\|\|'
t_NOT           = r'!'
t_IGUAL         = r'='
t_MASMAS        = r'\+\+'
t_MENOSMENOS    = r'--'
t_DOSPUNTO     = r':'
t_COMA         = r','
t_CORA         = r'\['
t_CORC         = r'\]'
t_PUNTO         = r'\.'

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        t.value = 0
    return t

def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value,'ID')
     return t

def t_CADENA(t):
    r'\"((?:[^"\\]|\\.)*)\"'
    t.value = t.value.replace("\\n", "\n").replace("\\t", "\t").replace("\\r", "\r").replace("\\\"", "\"").replace("\\\\", "\\").replace("\\\'", "\'")[1:-1]
    return t

def t_CARACTER(t):
    r"\'((?:[^'\\]|\\(t|\'|\n|\"|r|\\))*)\'"
    t.value = t.value[1:-1] # remuevo las comillas simples
    return t

#COMENTARIO MULTIPLE
def t_COMENTARIO_MULTIPLE(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    
# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r'//.*\n'
    t.lexer.lineno += 1



# Caracteres ignorados
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    errores.append(Excepcion("Lexico","Error léxico." + t.value[0] , t.lexer.lineno, find_column(input, t)))
    #print(str( t.value[0] )+ str(t.lexer.lineno)+":"+str(find_column(input, t)))
    #errores.append(Error(t.value[0],"LEXICO",t.lexer.lineno, find_column(input, t)))
    t.lexer.skip(1)

# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(inp, token):
    line_start = inp.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# Construyendo el analizador léxico
import ply.lex as lex

lexer = lex.lex(reflags = re.IGNORECASE)


#______________________ Asociación de operadores y precedencia ____________________________
precedence = (
    ('left','OR'),
    ('left','AND'),
    ('left','IGUALIGUAL','DISTINTO', 'MENOR','MENORIGUAL','MAYOR','MAYORIGUAL'),
    ('left','MAS','MENOS','COMA'),
    ('left','DIV','POR','MOD'),
    ('nonassoc','POT'),
    ('right','UNOT', 'UMENOS'),
    )



# Definición de la gramática

#_______________________________  Abstract ______________________________________
from Abstract.Instruccion import Instruccion
#_______________________________ TIPOS DE INSTRUCCION ___________________________
from Instrucciones.Imprimir import Imprimir
from Instrucciones.Declaracion import Declaracion
from Instrucciones.Declaracion_sinAsignacion import Declaracion_sinAsignacion
from Instrucciones.Asignacion import Asignacion
from Instrucciones.If import If
from Instrucciones.Break import Break
from Instrucciones.While import While
from Instrucciones.Incremento import Incremento
from Instrucciones.For import For
from Instrucciones.Continue import Continue
from Instrucciones.Funcion import Funcion
from Instrucciones.Return import Return
from Instrucciones.Llamada import Llamada
from Instrucciones.DeclaracionArreglo import DeclaracionArreglo
from Instrucciones.DeclaracionArreglo2 import DeclaracionArreglo2
from Instrucciones.ModificarArreglo import ModificarArreglo

#________________________________ OPERADORES Y TABLA SE SIMBOLO ___________________
from TS.Tipo import OperadorAritmetico, TIPO,OperadorRelacional,OperadorLogico,OperadorIncremento

#________________________________ TIPOS DE EXPRESIONES ____________________________
from Expresiones.Primitivos import Primitivos
from Expresiones.Aritmetica import Aritmetica
from Expresiones.Relacional import Relacional
from Expresiones.Logica import Logica
from Expresiones.Identificador import Identificador
from Expresiones.Casteo import Casteo
from Expresiones.AccesoArreglo import AccesoArreglo
from Expresiones.To_Fixed import To_Fixed
from Expresiones.To_Exponential import To_Exponential
from Expresiones.To_String import To_String
from Expresiones.To_LowerCase import To_LowerCase
from Expresiones.To_UpperCase import To_UpperCase
from Expresiones.Split import Split
from Expresiones.Length import Length

#___________________________________ REPORTE ______________________________________
from Reporte.Reporte import reporte

def p_init(t) :
    'init            : instrucciones'
    t[0] = t[1]

def p_instrucciones_instrucciones_instruccion(t) :
    'instrucciones    : instrucciones instruccion'
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]
    
#_______________________________________ INSTRUCCIONES _________________________________

def p_instrucciones_instruccion(t) :
    'instrucciones    : instruccion'
    if t[1] == "":
        t[0] = []
    else:    
        t[0] = [t[1]]

#_______________________________________ INSTRUCCION ___________________________________

def p_instruccion(t) :
    '''instruccion      : imprimir_instr
                        | declaracion
                        | declaracion_sinAsig
                        | asignacion
                        | if
                        | break 
                        | while
                        | tipo_incremento 
                        | for 
                        | continue
                        | funcion 
                        | retorno
                        | llamada
                        | declaracion_arreglo
                        | declaracion_arreglo2
                        | modificar_arreglo'''
    t[0] = t[1]

def p_instruccion_error(t):
    'instruccion        : error errores'
    errores.append(Excepcion("Sintáctico","Error Sintáctico." + str(t[1].value) , t.lineno(1), find_column(input, t.slice[1])))
    t[0] = ""

def p_instruccion_errores(t):
    '''errores : PUNTOCOMA
                | LLAVEC'''
    t[0] = t[1]

#_______________________________________ IMPRIMIR ______________________________________

def p_imprimir(t) :
    'imprimir_instr : Rconsole PUNTO Rlog PARA imprimir_listas PARC fin_instr'
    print()
    t[0] = Imprimir(t[5], t.lineno(1), find_column(input, t.slice[1]))

def p_imprimir_listas(t) :
    'imprimir_listas : imprimir_listas COMA expresion'
    if t[3] != "":
        t[1].append(t[3])
    t[0] = t[1]

def p_imprimir_lista(t) :
    'imprimir_listas : expresion '
    t[0] = [t[1]]


#_______________________________________ DECLARACION __________________________________
def p_declaracion(t):
    'declaracion     : Rlet ID DOSPUNTO tipo IGUAL expresion fin_instr'
    t[0] = Declaracion(t[4], t[2], t.lineno(2), find_column(input, t.slice[2]), t[6])

#_______________________________________ DECLARACION ANY__________________________________
def p_declaracion_any(t):
    'declaracion     : Rlet ID IGUAL expresion fin_instr'
    t[0] = Declaracion(None, t[2], t.lineno(2), find_column(input, t.slice[2]), t[4])

def p_tipo(t):
    '''tipo : Rnumber
            | Rboolean
            | Rstring 
            | Rany
            | Rvoid'''

    if t[1] == 'number':
        t[0] = TIPO.NUMBER
    elif t[1] == 'string':
        t[0] = TIPO.STRING
    elif t[1] == 'boolean':
        t[0] = TIPO.BOOLEAN
    elif t[1] == 'any':
        t[0] = TIPO.ANY
    elif t[1] == 'void':
        t[0] = TIPO.VOID


#_______________________________________DECLARACION SIN ASIGNAION ________________________
def p_declaracionsinAsignacion(t) :
    ''' declaracion_sinAsig : Rlet ID DOSPUNTO tipo fin_instr '''
    t[0] = Declaracion_sinAsignacion(t[4],t[2],t.lineno(2), find_column(input, t.slice[2]))

#_______________________________________DECLARACION SIN ASIGNAION ANY________________________
def p_declaracionsinAsignacion_any(t) :
    ''' declaracion_sinAsig : Rlet ID fin_instr '''
    t[0] = Declaracion_sinAsignacion(None,t[2],t.lineno(2), find_column(input, t.slice[2]))


#_______________________________________ ASIGNACION ______________________________________
def p_asignacion(t):
    ''' asignacion : ID IGUAL  expresion fin_instr'''
    t[0] =  Asignacion(t[1],t[3],t.lineno(1), find_column(input, t.slice[1]))


#_______________________________________ IF _________________________________________
def p_if(t) :
    'if     : Rif PARA expresion PARC LLAVEA instrucciones LLAVEC'
    t[0] = If(t[3], t[6], None, None, t.lineno(1), find_column(input, t.slice[1]))

def p_if_else(t) :
    'if     : Rif PARA expresion PARC LLAVEA instrucciones LLAVEC Relse LLAVEA instrucciones LLAVEC'
    t[0] = If(t[3], t[6], t[10], None, t.lineno(1), find_column(input, t.slice[1]))

def p_if_elseIf_else(t) :
    'if     : Rif PARA expresion PARC LLAVEA instrucciones LLAVEC Relse if'
    t[0] = If(t[3], t[6], None, t[9], t.lineno(1), find_column(input, t.slice[1]))


#______________________________________ BREAK ________________________________________
def p_break(t):
    'break : Rbreak fin_instr'
    t[0] = Break(t.lineno(1), find_column(input, t.slice[1]))


#______________________________________ WHILE _______________________________________
def p_while(t):
    ''' while : Rwhile PARA expresion PARC LLAVEA instrucciones LLAVEC '''
    t[0] = While(t[3],t[6],t.lineno(1), find_column(input, t.slice[1]))



#______________________________________ TIPO INCREMENTO _____________________________
def p_incrementos(t):
    ''' tipo_incremento : ID MASMAS fin_instr
                        | ID MENOSMENOS fin_instr '''
    if t[2]=='++':
        t[0] = Incremento(t[1],OperadorIncremento.MASMAS,t.lineno(1), find_column(input, t.slice[1]))
    elif t[2]=='--':
        t[0] = Incremento(t[1],OperadorIncremento.MENOSMENOS,t.lineno(1), find_column(input, t.slice[1]))


#_______________________________________    FOR _____________________________________
def p_for(t):
    ''' for : Rfor PARA declar_asig expresion fin_instr actualizacion PARC LLAVEA instrucciones LLAVEC'''
    t[0] = For(t[3],t[4],t[6],t[9],t.lineno(1), find_column(input, t.slice[1]))

def p_declaracion_asig(t):
    ''' declar_asig : declaracion
                    | asignacion '''
    t[0] = t[1]
def p_actualizacion_asig(t):
    '''actualizacion : asignacion
                    |  tipo_incremento'''
    t[0] = t[1]

#_______________________________________ CONTINUE ___________________________________
def p_continue(t):
    '''continue : Rcontinue fin_instr'''
    t[0] = Continue(t.lineno(1), find_column(input, t.slice[1]))


#_______________________________________ PUNTO COMA __________________________________
def p_puntocoma(t):
    ''' fin_instr : PUNTOCOMA
                    | '''
    t[0]=None


#_______________________________________ FUNCION ______________________________________
def p_funcion(t):
    ''' funcion : Rfunc ID PARA parametros PARC DOSPUNTO tipo LLAVEA instrucciones LLAVEC '''
    t[0]=Funcion(t[7],t[2],t[4],t[9],t.lineno(1), find_column(input, t.slice[1]))

def p_funcion_noparam(t):
    '''funcion : Rfunc ID PARA PARC DOSPUNTO tipo LLAVEA instrucciones LLAVEC'''
    t[0]=Funcion(t[6],t[2],[],t[8],t.lineno(1), find_column(input, t.slice[1]))

def p_funcionSinTipo(t):
    ''' funcion : Rfunc ID PARA parametros PARC LLAVEA instrucciones LLAVEC '''
    t[0]=Funcion(TIPO.VOID,t[2],t[4],t[7],t.lineno(1), find_column(input, t.slice[1]))

def p_funcion_noparamSinTipo(t):
    '''funcion : Rfunc ID PARA PARC LLAVEA instrucciones LLAVEC'''
    t[0]=Funcion(TIPO.VOID,t[2],[],t[6],t.lineno(1), find_column(input, t.slice[1]))

def p_paramtros(t):
    '''parametros : parametros COMA parametro'''
    t[1].append(t[3])
    t[0] = t[1]

def p_parametro_1(t):
    '''parametros : parametro'''
    t[0] = [t[1]]

def p_parametro(t):
    '''parametro : ID DOSPUNTO tipo'''
    t[0] = {'tipo':t[3],'identificador':t[1]}

def p_parametro_Arr(t):
    '''parametro : ID DOSPUNTO tipo lista_Dim  '''
    t[0] = {'tipo':t[3],'identificador':t[1]}

#_________________________________________RETURN _______________________________________
def p_retorno(t):
    ''' retorno : Rreturn expresion fin_instr '''
    t[0]= Return(t[2],t.lineno(1), find_column(input, t.slice[1]))

#_______________________________________ LLAMADA _____________________________________
def p_llamada(t):
    ''' llamada : ID PARA parametros_llamada PARC fin_instr '''
    t[0]=Llamada(t[1],t[3],t.lineno(1), find_column(input, t.slice[1]))

def p_llamada_sinp(t):
    ''' llamada : ID PARA PARC fin_instr'''
    t[0]=Llamada(t[1],[],t.lineno(1), find_column(input, t.slice[1]))

def p_parametros_llamada(t):
    '''parametros_llamada : parametros_llamada COMA parametro_llam'''
    t[1].append(t[3])
    t[0]=t[1]
def p_parametros(t):
    '''parametros_llamada : parametro_llam'''
    t[0]=[t[1]]

def p_parametro_llam(t):
    '''parametro_llam : expresion'''
    t[0]=t[1]

#_______________________________________ DECLARACION ARREGLO _________________________

def p_tipo1_arregloTipo(t):
    '''declaracion_arreglo : Rlet ID DOSPUNTO tipo lista_expresiones fin_instr'''
    t[0] = DeclaracionArreglo(t[2],t[4],t[5],t.lineno(3), find_column(input, t.slice[3]))
    #let id : tipo [3][3][3]  ->generacion de la expresion

def p_lista_Dim1(t) :
    'lista_Dim     : lista_Dim CORA CORC'
    t[0] = t[1] + 1
    
def p_lista_Dim2(t) :
    'lista_Dim    : CORA CORC'
    t[0] = 1

def p_lista_expresiones_1(t) :
    'lista_expresiones     : lista_expresiones CORA expresion CORC'
    t[1].append(t[3])
    t[0] = t[1]
    
def p_lista_expresiones_2(t) :
    'lista_expresiones    : CORA expresion CORC'
    t[0] = [t[2]]

#____________________________ ARREGLO TIPO 2 _______________________________________

def p_tipo2_arreglo(t):
    '''declaracion_arreglo2 : Rlet ID IGUAL CORA tipo_lista CORC fin_instr'''
    t[0] = DeclaracionArreglo2(TIPO.ANY,1,t[2],t[5],t.lineno(3), find_column(input, t.slice[3]))
    #let arr = [1,2,3,4,5,6]
    

def p_tipo2_arregloSinDimensiones(t):
    '''declaracion_arreglo2 : Rlet ID DOSPUNTO tipo lista_Dim IGUAL CORA tipo_lista CORC fin_instr'''
    t[0] = DeclaracionArreglo2(t[1],1,t[2],t[5],t.lineno(3), find_column(input, t.slice[3]))
    #let arr : number [] = [1,2,3,4,5,6,7,8,9,10] 
    

def p_tipo2_arregloConDimensiones(t):
    '''declaracion_arreglo2 : Rlet ID DOSPUNTO tipo lista_expresiones IGUAL CORA tipo_lista CORC fin_instr'''
    t[0] = DeclaracionArreglo2(TIPO.ANY,1,t[2],t[5],t.lineno(3), find_column(input, t.slice[3]))
    #let arr[5] = [1,2,3,4,5]
    
def p_tipo2_arreglo_asig(t):
    '''declaracion_arreglo2 : tipo lista_Dim ID IGUAL ID'''
    t[0] = DeclaracionArreglo2(t[1],t[2],t[3],Identificador(t[5],t.lineno(5), find_column(input, t.slice[5])),t.lineno(3), find_column(input, t.slice[3]))

def p_tipo_listad1(t):
    '''tipo_lista : d1'''
    t[0] = t[1]

def p_tipo_listad2(t):
    '''tipo_lista : d2'''
    t[0] = t[1]

def p_tipo_listad3(t):
    '''tipo_lista : d3'''
    t[0] = t[1]

def p_d1(t):
    '''d1 : d1 COMA expresion'''
    t[1].append(t[3])
    t[0]=t[1]

def p_d11(t):
    '''d1 : expresion'''
    t[0] = [t[1]]

def p_d2(t):
    '''d2 : d2 COMA LLAVEA d1 LLAVEC'''
    t[1].append(t[4])
    t[0]=t[1]

def p_d21(t):
    '''d2 : LLAVEA d1 LLAVEC'''
    t[0] = [t[2]]

def p_d3(t):
    '''d3 : d3 COMA LLAVEA d2 LLAVEC'''
    t[1].append(t[4])
    t[0]=t[1]

def p_d31(t):
    '''d3 : LLAVEA d2 LLAVEC'''
    t[0]=[t[2]]

#__________________________________ MODIFICAR ARREGLO _______________________________
def p_modificar_arreglo(t):
    '''modificar_arreglo :  ID lista_expresiones IGUAL expresion fin_instr'''
    t[0] = ModificarArreglo(t[1],t[2],t[4],t.lineno(1), find_column(input, t.slice[1]))


#_______________________________________ EXPRESION ____________________________________

def p_expresion_binaria(t):
    '''
    expresion : expresion MAS expresion
            | expresion MENOS expresion
            | expresion POR expresion
            | expresion DIV expresion
            | expresion POT expresion
            | expresion MOD expresion
            | expresion MENORIGUAL expresion
            | expresion MENOR expresion
            | expresion MAYORIGUAL expresion
            | expresion MAYOR expresion
            | expresion IGUALIGUAL expresion
            | expresion DISTINTO expresion
            | expresion AND expresion
            | expresion OR expresion
    '''
    if t[2] == '+':
        t[0] = Aritmetica(OperadorAritmetico.MAS, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '-':
        t[0] = Aritmetica(OperadorAritmetico.MENOS, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '*':
        t[0] = Aritmetica(OperadorAritmetico.POR,t[1],t[3],t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '/':
        t[0] = Aritmetica(OperadorAritmetico.DIV, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '**':
        t[0] = Aritmetica(OperadorAritmetico.POT,t[1],t[3],t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '%':
        t[0] = Aritmetica(OperadorAritmetico.MOD,t[1],t[3],t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '<':
        t[0] = Relacional(OperadorRelacional.MENOR,t[1],t[3],t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '<=':
        t[0] = Relacional(OperadorRelacional.MENORIGUAL,t[1],t[3],t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>':
        t[0] = Relacional(OperadorRelacional.MAYOR,t[1],t[3],t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>=':
        t[0] = Relacional(OperadorRelacional.MAYORIGUAL,t[1],t[3],t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '===':
        t[0] = Relacional(OperadorRelacional.IGUALIGUAL,t[1],t[3],t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '!==':
        t[0] = Relacional(OperadorRelacional.DISTINTO,t[1],t[3],t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '&&':
        t[0] = Logica(OperadorLogico.AND,t[1],t[3],t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '||':
        t[0] = Logica(OperadorLogico.OR,t[1],t[3],t.lineno(2), find_column(input, t.slice[2]))
    
  
def p_expresion_unaria(t):
    '''
    expresion : MENOS expresion %prec UMENOS 
            | NOT expresion %prec UNOT 
    '''
    if t[1] == '-':
        t[0] = Aritmetica(OperadorAritmetico.UMENOS, t[2],None, t.lineno(1), find_column(input, t.slice[1]))
    elif t[1] == '!':
        t[0] = Logica(OperadorLogico.NOT, t[2],None, t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_parentesis(t):
    ''' expresion : PARA expresion PARC '''
    t[0] = t[2]

def p_expresion_entero(t):
    '''expresion : ENTERO'''
    t[0] = Primitivos(TIPO.NUMBER,t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_decimal(t):
    '''expresion : DECIMAL'''
    t[0] = Primitivos(TIPO.NUMBER, t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_cadena(t):
    '''expresion : CADENA'''
    t[0] = Primitivos(TIPO.STRING,str(t[1]).replace('\\n', '\n'), t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_true(t):
    '''expresion : Rtrue'''
    t[0] = Primitivos(TIPO.BOOLEAN,True,t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_false(t):
    '''expresion : Rfalse'''
    t[0] = Primitivos(TIPO.BOOLEAN,False,t.lineno(1), find_column(input, t.slice[1]))

def p_identificador(t):
    '''expresion : ID '''
    t[0] = Identificador(t[1],t.lineno(1), find_column(input, t.slice[1]))

def p_null(t):
    '''expresion : Rnull '''
    t[0] = Primitivos(TIPO.NULL_,None,t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_llam(t):
    ''' expresion : llamada'''
    t[0]=t[1]

def p_casteo(t):
    ''' expresion : PARA tipo PARC expresion '''
    t[0] = Casteo(t[2],t[4],t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_arreglo(t):
    '''expresion : ID lista_expresiones'''
    t[0] = AccesoArreglo(t[1],t[2],t.lineno(1), find_column(input, t.slice[1]))

#_________________________________ EXPRESIONES PARA NATIVAS _________________
def p_expresion_toFixed(t):
    '''expresion : ID PUNTO RtoFixed PARA expresion PARC'''
    t[0] = To_Fixed(t[1],t[5],t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_toExponential(t):
    '''expresion : ID PUNTO RtoExponential PARA expresion PARC'''
    t[0] = To_Exponential(t[1],t[5],t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_toString(t):
    '''expresion : ID PUNTO RtoString PARA PARC'''
    t[0] = To_String(t[1],t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_toLowerCase(t):
    '''expresion : ID PUNTO RtoLowerCase PARA PARC'''
    t[0] = To_LowerCase(t[1],t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_toUpperCase(t):
    '''expresion : ID PUNTO RtoUpperCase PARA PARC'''
    t[0] = To_UpperCase(t[1],t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_Length(t):
    '''expresion : ID PUNTO Rlength PARA PARC'''
    t[0] = Length([1],t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_Split(t):
    '''expresion : ID PUNTO Rsplit PARA expresion PARC'''
    t[0] = Split(t[1],t[5],t.lineno(1), find_column(input, t.slice[1]))

import ply.yacc as yacc
parser = yacc.yacc()

input = ''

def getErrores():
    return errores

def parse(inp) :
    global errores
    global lexer
    global parser
    errores = []
    lexer = lex.lex()
    parser = yacc.yacc()
    global input
    input = inp
    return parser.parse(inp)

#INTERFAZ



