import ply.yacc as yacc
from Analizador_Lexico import tokens, lexer, errores, find_column
from src.Expresiones.aritmetica import Aritmetica
from src.Expresiones.primitivos import Primitivos
from src.Expresiones.relacional import Relacionales
from src.Expresiones.logicas import Logicas
from src.Instrucciones.imprimir import Imprimir
from src.Instrucciones.declaracion import Declaracion
from src.Instrucciones.asignacion import Asignacion
from src.Instrucciones.IF import If
from src.Tabla_Simbolos.tabla_simbolos import TablaSimbolos
from src.Tabla_Simbolos.arbol import Arbol
from src.Tabla_Simbolos.Exception import Exception
from src.Expresiones.identificador import Identificador
from src.Abstract.Tipo import TIPO
from src.Abstract.Tipo import NATIVA
from src.Expresiones.IncDec import IncDec
from src.Expresiones.nativas import Nativas
from src.Instrucciones.For import For
from src.Instrucciones.WHILE import While
from src.Instrucciones.Break_Continue import Break
from src.Instrucciones.Break_Continue import Continue
from src.Instrucciones.FUNCION import Function
from src.Instrucciones.Llamada import Llamada
from src.Instrucciones.Return import Return

from src.Tabla_Simbolos.generador import Generador
import sys
tsg = None
ast = None
limit = sys.getrecursionlimit()
#print('Before changing, limit of stack =', limit)
# New limit
Newlimit = 5000
# Using sys.setrecursionlimit() method
sys.setrecursionlimit(Newlimit)

precedence = (
    ('left', 'RTor'),
    ('left', 'RTand'),
    ('right', 'UNOT'),  # !

    ('left', 'RTigualacion', 'RTdistinto'),
    ('left', 'RTmenor', 'RTmenor_igual', 'RTmayor', 'RTmayor_igual'),
    ('left', 'RTmas', 'RTmenos'),
    ('left', 'RTmasmas', 'RTmenosmenos'),  #RTcoma?
    ('left', 'RTpor', 'RTdiv', 'RTmodulo'),  #add MOD
    ('right', 'RTpotencia'),
    ('left', 'RTpa', 'RTpc'),
    ('right', 'UMENOS'),
)

# Definicion de la Gramatica
def p_init(t):
    'INIT : INSTRUCCIONES'
    t[0] = t[1]


def p_instrucciones_lista(t):
    'INSTRUCCIONES    : INSTRUCCIONES INSTRUCCION'
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]

def p_instrucciones_2(t):
    'INSTRUCCIONES : INSTRUCCION'

    if t[1] == "":
        t[0] = []
    else:
        t[0] = [t[1]]

def p_instrucciones_evaluar(t):
    '''INSTRUCCION : IMPRIMIR RTptcoma
                    | DECLARACION_NORMAL RTptcoma
                    | IFS RTptcoma
                    | FOR RTptcoma
                    | INCRDECR RTptcoma
                    | ASIGNACION RTptcoma
                    | WHILE RTptcoma
                    | TRANSFERENCIA RTptcoma
                    | FUNCION RTptcoma
                    | LLAMADA_FUNCION RTptcoma
                    | RETORNO RTptcoma'''
    t[0] = t[1]

def p_instrucciones_evaluar2(t):
    '''INSTRUCCION : IMPRIMIR
                    | DECLARACION_NORMAL
                    | IFS
                    | FOR
                    | INCRDECR
                    | ASIGNACION
                    | WHILE
                    | TRANSFERENCIA
                    | FUNCION
                    | LLAMADA_FUNCION
                    | RETORNO'''
    t[0] = t[1]



def p_retorno(t):
    '''RETORNO : RTreturn EXPRESION
               | RTreturn RTllavea EXPRESION RTllavec
               | RTreturn'''

    if len(t) == 3:
        t[0] = Return(t[2], t.lineno(1), find_column(input, t.slice[1]))
    elif len(t) == 5:
        t[0] = Return(t[3], t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = Return(None, t.lineno(1), find_column(input, t.slice[1]))

def p_llamada_funcion(t):
    '''LLAMADA_FUNCION : RTid RTpa RTpc
                       | RTid RTpa PARAMETROS_LLAMADA RTpc'''
    if len(t)== 4: # funciona como en un arreglo tamanio = 3 -> 0, 1, 2
        t[0] = Llamada(t[1], None, t.lineno(1), find_column(input, t.slice[1]))
    elif len(t) == 5:
        t[0] = Llamada(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))

def p_instrucciones_funcion(t):
    '''FUNCION : RTfunction RTid RTpa RTpc RTllavea INSTRUCCIONES RTllavec
               | RTfunction RTid RTpa RTpc RTdpuntos RTvoid RTllavea INSTRUCCIONES RTllavec
               | RTfunction RTid RTpa PARAMETROS RTpc RTllavea INSTRUCCIONES RTllavec
               | RTfunction RTid RTpa RTpc RTdpuntos TIPO RTllavea INSTRUCCIONES RTllavec
               | RTfunction RTid RTpa RTpc RTdpuntos RTid RTllavea INSTRUCCIONES RTllavec
               | RTfunction RTid RTpa PARAMETROS RTpc RTdpuntos TIPO RTllavea INSTRUCCIONES RTllavec
               | RTfunction RTid RTpa PARAMETROS RTpc RTdpuntos RTid RTllavea INSTRUCCIONES RTllavec
               | RTfunction RTid RTpa PARAMETROS RTpc RTdpuntos RTvoid RTllavea INSTRUCCIONES RTllavec'''
    if len(t) == 8:
        t[0] = Function(t[2], None, t[6], t.lineno(1), find_column(input, t.slice[1]), None)
    elif len(t) == 9:
        t[0] = Function(t[2], t[4], t[7], t.lineno(1), find_column(input, t.slice[1]), None)
    elif len(t) == 10:
        if t[6] == 'void':
            t[0] = Function(t[2], None, t[8], t.lineno(1), find_column(input, t.slice[1]), None)
        else:
            t[0] = Function(t[2], None, t[8], t.lineno(1), find_column(input, t.slice[1]), t[6])
    elif len(t) == 11:
        t[0] = Function(t[2], t[4], t[9], t.lineno(1), find_column(input, t.slice[1]), t[7])


def p_parametros_funcion(t):
    '''PARAMETROS : PARAMETROS RTcoma PARAMETRO
                  | PARAMETRO'''
    if len(t) == 4:
        t[1].append(t[3])
        t[0] = t[1]
    elif len(t) == 2:
        t[0] = [t[1]]

def p_parametros_funcion2(t):
    '''PARAMETRO : RTlet RTid RTdpuntos TIPO
                | RTconst RTid RTdpuntos TIPO
                | RTid RTdpuntos TIPO
                | RTid'''
    if len(t) == 2:
        t[0] = {'tipo': TIPO.ANY, 'id': t[1]}
    elif len(t) == 4:
        t[0] = {'tipo': t[3], 'id': t[1]}
    elif len(t) == 5:
        t[0] = {'tipo': t[4], 'id': t[2]}

def p_parametros_llamada(t):
    '''PARAMETROS_LLAMADA : PARAMETROS_LLAMADA RTcoma PARAMETRO_LLAMADA
                          | PARAMETRO_LLAMADA'''
    if len(t) == 4:
        t[1].append(t[3])
        t[0] = t[1]
    elif len(t) == 2:
        t[0] = [t[1]]

def p_parametros_llamada2(t):
    '''PARAMETRO_LLAMADA : EXPRESION'''
    t[0] = t[1]
def p_sentencias_transferencia(t):
    '''TRANSFERENCIA : RTbreak
                     | RTcontinue'''
    if t[1] == 'break':
        t[0] = Break(t.lineno(1), find_column(input, t.slice[1]))
    elif t[1] == 'continue':
        t[0] = Continue(t.lineno(1), find_column(input, t.slice[1]))

def p_while(t):
    'WHILE : RTwhile RTpa EXPRESION RTpc RTllavea INSTRUCCIONES RTllavec'
    t[0] = While(t[3], t[6], t.lineno(1), find_column(input, t.slice[1]))

def p_asignacion(t):
    'ASIGNACION : RTid RTigual EXPRESION'
    t[0] = Asignacion(t[1],t[3], t.lineno(1), find_column(input, t.slice[1]))

def p_imprimir(t):
    'IMPRIMIR : RTconsole RTpunto RTlog RTpa LISTA RTpc'
    t[0] = Imprimir(t[5], t.lineno(2), find_column(input, t.slice[2]))

def p_lista_imprimir(t):
    '''LISTA : LISTA RTcoma EXPRESION
            | EXPRESION'''
    if len(t) == 4:
        t[1].append(t[3])
        t[0] = t[1]
    elif len(t) == 2:
        t[0] = [t[1]]

def p_declaracion_normal(t):
    '''DECLARACION_NORMAL : RTlet RTid RTdpuntos TIPO RTigual EXPRESION
                          | RTconst RTid RTdpuntos TIPO RTigual EXPRESION'''
    t[0] = Declaracion(t[2],t[4],t[6],t.lineno(1),find_column(input, t.slice[1]))

def p_declaracion_normal_2(t):
    '''DECLARACION_NORMAL : RTlet RTid RTdpuntos TIPO
                          | RTconst RTid RTdpuntos TIPO'''

    tmp_exp2=0
    if t[4] == TIPO.BOOLEAN :
        tmp_exp2 = Primitivos(t[4], False, t.lineno(1), find_column(input, t.slice[1]))
    elif t[4] == TIPO.STRING or t[4] == TIPO.ANY :
        tmp_exp2 = Primitivos(t[4], str(''), t.lineno(1), find_column(input, t.slice[1]))
    elif t[4] == TIPO.NUMBER :
        tmp_exp2 = Primitivos(t[4], int(0), t.lineno(1), find_column(input, t.slice[1]))

    t[0] = Declaracion(t[2], t[4], tmp_exp2, t.lineno(1), find_column(input, t.slice[1]))

def p_declaracion_imple(t):
    '''DECLARACION_NORMAL : RTlet RTid
                          | RTconst RTid'''
    tmp_exp = Primitivos(TIPO.ANY, str(''), t.lineno(1), find_column(input, t.slice[1]))
    t[0] = Declaracion(t[2],TIPO.ANY,tmp_exp,t.lineno(1),find_column(input, t.slice[1]))

def p_declaracion_simple2(t):
    '''DECLARACION_NORMAL : RTlet RTid RTigual EXPRESION
                          | RTconst RTid RTigual EXPRESION'''
    t[0] = Declaracion(t[2],TIPO.ANY,t[4],t.lineno(1),find_column(input, t.slice[1]))

def p_expresion_funcion(t):
    'EXPRESION : LLAMADA_FUNCION'
    t[0] = t[1]

def p_ifs(t):
    'IFS : RTif IF'
    t[0] = t[2]
def p_condicional_if(t):
    'IF : RTpa EXPRESION RTpc RTllavea INSTRUCCIONES RTllavec'
    t[0] = If(t[2], t[5], None, None, t.lineno(1), find_column(input, t.slice[1]))

def p_condicional_if_else(t):
    'IF : RTpa EXPRESION RTpc RTllavea INSTRUCCIONES RTllavec RTelse RTllavea INSTRUCCIONES RTllavec'
    t[0] = If(t[2], t[5], t[9], None, t.lineno(1), find_column(input, t.slice[1]))

def p_condicional_if_else_if(t):
    'IF : RTpa EXPRESION RTpc RTllavea INSTRUCCIONES RTllavec RTelse IFS'
    t[0] = If(t[2], t[5], None, t[8], t.lineno(1), find_column(input, t.slice[1]))

def p_ciclo_for(t):
    'FOR : RTfor RTpa DECLARACION_NORMAL RTptcoma EXPRESION RTptcoma INCRDECR RTpc RTllavea INSTRUCCIONES RTllavec'
    t[0] = For(t.lineno(1), find_column(input, t.slice[1]),t[3], t[5], t[7], t[10])

def p_incrDecr(t):
    '''INCRDECR : EXPRESION RTmasmas
        | EXPRESION RTmenosmenos
    '''
    t[0]=IncDec(t.lineno(2), find_column(input, t.slice[2]),t[2],t[1])


def p_tipo(t):
    '''TIPO : RTstring
            | RTnumber
            | RTboolean
            | RTvoid'''
    if t[1] =='string':
        t[0] = TIPO.STRING
    elif t[1] == 'number':
        t[0] = TIPO.NUMBER
    elif t[1] == 'boolean':
        t[0] = TIPO.BOOLEAN
    
def p_expresion_binaria(t):
    '''EXPRESION : EXPRESION RTmas EXPRESION
                | EXPRESION RTmenos EXPRESION
                | EXPRESION RTpor EXPRESION
                | EXPRESION RTdiv EXPRESION
                | EXPRESION RTmodulo EXPRESION
                | EXPRESION RTpotencia EXPRESION'''
    if t[2] == '+':
        t[0] = Aritmetica(t[1], t[3], '+', t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '-':
        t[0] = Aritmetica(t[1], t[3], '-', t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '*': 
        t[0] = Aritmetica(t[1], t[3], '*', t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '/': 
        t[0] = Aritmetica(t[1], t[3], '/', t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '%': #^
        t[0] = Aritmetica(t[1], t[3], '%', t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '^': #^
        t[0] = Aritmetica(t[1], t[3], '^', t.lineno(2), find_column(input, t.slice[2]))

def p_expresion2(t): # E -> (E)
    'EXPRESION : RTpa EXPRESION RTpc'
    t[0] = t[2]
def p_relacionales(t):
    '''EXPRESION : EXPRESION RTmayor EXPRESION
                | EXPRESION RTmenor EXPRESION
                | EXPRESION RTmayor_igual EXPRESION
                | EXPRESION RTmenor_igual EXPRESION
                | EXPRESION RTdistinto EXPRESION
                | EXPRESION RTigualacion EXPRESION'''
    t[0] = Relacionales(t[1],t[3],t[2], t.lineno(2), find_column(input, t.slice[2]))

def p_logicas(t):
    '''EXPRESION : EXPRESION RTor EXPRESION
                | EXPRESION RTand EXPRESION
                | RTnot EXPRESION %prec UNOT'''
    if  t[1] == '!':
        t[0] = Logicas(None,t[2],t[1], t.lineno(1), find_column(input, t.slice[1]))
    else :
        t[0] = Logicas(t[1],t[3],t[2], t.lineno(2), find_column(input, t.slice[2]))

def p_funcion_nativa(t):
    '''
    EXPRESION : RTid RTpunto RTtoFixed RTpa EXPRESION RTpc
              | RTid RTpunto RTtoExp RTpa EXPRESION RTpc
              | RTid RTpunto RTtoStr RTpa RTpc
              | RTid RTpunto RTtoLower RTpa RTpc
              | RTid RTpunto RTtoUpper RTpa RTpc
              | RTid RTpunto RTsplit RTpa EXPRESION RTpc
              | RTtype RTpa EXPRESION RTpc
    '''
    ident = Identificador(t[1], None, t.lineno(1), find_column(input, t.slice[1]), None)
    if t[3] == 'toFixed':
        t[0] = Nativas(ident, NATIVA.APROXIMACION, t[5], t.lineno(1), find_column(input, t.slice[1]))
    elif t[3] == 'toExponential':
        t[0] = Nativas(ident, NATIVA.EXPONENCIAL, t[5], t.lineno(1), find_column(input, t.slice[1]))
    elif t[3] == 'toString':
        t[0] = Nativas(ident, NATIVA.STRING, None, t.lineno(1), find_column(input, t.slice[1]))
    elif t[3] == 'toLowerCase':
        t[0] = Nativas(ident, NATIVA.LOWER, None, t.lineno(1), find_column(input, t.slice[1]))
    elif t[3] == 'toUpperCase':
        t[0] = Nativas(ident, NATIVA.UPPER, None, t.lineno(1), find_column(input, t.slice[1]))
    elif t[3] == 'split':
        t[0] = Nativas(ident, NATIVA.SPLIT, t[5], t.lineno(1), find_column(input, t.slice[1]))
    elif t[1] == 'typeof':
        t[0] = Nativas(None, NATIVA.TYPEOF, t[3], t.lineno(1), find_column(input, t.slice[1]))
def p_expresion_unaria(t):
    'EXPRESION : RTmenos EXPRESION %prec UMENOS'
    tmp_num = Primitivos(TIPO.NUMBER, 0, t.lineno(1), find_column(input, t.slice[1]))
    t[0] = Aritmetica(tmp_num, t[2], '-', t.lineno(1), find_column(input, t.slice[1]))
    
def p_identificador(t):
    'EXPRESION : RTid'
    t[0] = Identificador(t[1], None, t.lineno(1), find_column(input, t.slice[1]), None)

def p_expresion_entero(t):
    'EXPRESION : RTnumero'
    t[0] = Primitivos(TIPO.NUMBER, int(t[1]), t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_decimal(t):
    'EXPRESION : RTdecimal'
    t[0] = Primitivos(TIPO.NUMBER, float(t[1]), t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_cadena(t):
    'EXPRESION : RTcadena'
    t[0] = Primitivos(TIPO.STRING, str(t[1]), t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_boolean(t):
    '''EXPRESION : RTtrue
                | RTfalse'''
    if t[1] == 'true':
        t[0] = Primitivos(TIPO.BOOLEAN, True, t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = Primitivos(TIPO.BOOLEAN, False, t.lineno(1), find_column(input, t.slice[1]))

        
def p_error(t):
    #print(" Error sintáctico en '%s'" % t.value)
     # get formatted representation of stack
    stack_state_str = ' '.join([symbol.type for symbol in parser.symstack][1:])

    print('Syntax error in input! Parser State:{} {} . {}'
          .format(parser.state,
                  stack_state_str,
                  t))

input = ''

def parse(inp):
    global errores
    global parser
    errores = []
    parser = yacc.yacc()
    global input
    input = inp
    lexer.lineno = 1
    return parser.parse(inp)


entrada = '''
let a:boolean = true && true;
console.log(a);
console.log(a);
'''

def test_lexer(lexer):
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        # print(tok)

lexer.input(entrada)
test_lexer(lexer)

def ejecutar_entrada(entrada):
    generador = Generador()
    generador = generador.getInstance()
    generador.cleanAll()
    # genAux = None
    # genAux = Generador()
    # genAux.cleanAll(); # Limpia todos los archivos anteriores
    # generador = None
    # generador = genAux.getInstance()

    global tsg
    global ast    

    instrucciones = parse(entrada)
    ast = Arbol(instrucciones)
    tsg = TablaSimbolos()
    ast.setTsglobal(tsg)

    for instruccion in ast.getInstr():
        #if not (isinstance(instruccion, Function)):
        value = instruccion.interpretar(ast, tsg)
        if isinstance(value, Exception):
            ast.getErrores().append(value)
                # aqui es opcional el que se muestren los errores en consola
                # ast.updateConsola(value.toString())
    print(ast.getTablaReporte())
    return generador.getCode()

def getTablaSimbolos():
    return ast.getTablaReporte()

def getErrores():
    for err in ast.getErrores():
        print(err)

