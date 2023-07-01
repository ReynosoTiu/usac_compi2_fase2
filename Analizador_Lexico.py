import re
import ply.lex as lex

errores = []

reserved = {
    'console'     :   'RTconsole',
    'log'         :   'RTlog',
    'let'         :   'RTlet',
    'string'      :   'RTstring',
    'number'      :   'RTnumber',
    'boolean'     :   'RTboolean',
    'true'        :   'RTtrue',
    'false'       :   'RTfalse',
    'else'        :   'RTelse',
    'if'          :   'RTif',
    'for'         :   'RTfor',
    'toFixed'     :   'RTtoFixed',
    'toExponential':  'RTtoExp',
    'toString':       'RTtoStr',
    'toLowerCase':    'RTtoLower',
    'toUpperCase':    'RTtoUpper',
    'split':          'RTsplit',
    'while':          'RTwhile',
    'break':          'RTbreak',
    'continue':       'RTcontinue',
    'function':       'RTfunction',
    'return':         'RTreturn',
    'void':           'RTvoid',
    'typeof':         'RTtype',
    'const':          'RTconst',
}

tokens  = [
    #Relacionales
    'RTmayor_igual',
    'RTmenor_igual', 
    'RTigualacion',
    'RTdistinto',
    'RTmayor',    
    'RTmenor',    

    #Logicas
    'RTor',
    'RTand',
    'RTnot',

    #aritmeticas
    'RTpotencia',
    'RTmodulo',
    'RTmas',
    'RTmenos',
    'RTpor',
    'RTdiv',
    'RTmasmas',
    'RTmenosmenos',

    'RTcoma',
    'RTpunto',
    'RTdpuntos',
    'RTptcoma',
    'RTpa',
    'RTpc',
    'RTllavea',
    'RTllavec',
    'RTigual',
    'RTnumero',
    'RTdecimal',
    'RTcadena',
    'RTid'
]+ list(reserved.values())
# Tokens
#Relacionales
t_RTmayor_igual   = r'\>='
t_RTmenor_igual   = r'\<='
t_RTigualacion    = r'\==='
t_RTdistinto      = r'\!=='
t_RTmayor         = r'\>'
t_RTmenor         = r'\<'

#Logicas
t_RTor            = r'\|\|'
t_RTand           = r'\&&'
t_RTnot           = r'\!'

#Aritmeticas
t_RTpotencia      = r'\^'
t_RTmodulo        = r'\%'
t_RTmasmas        = r'\+\+'
t_RTmenosmenos    = r'\-\-'
t_RTmas           = r'\+'
t_RTmenos         = r'\-'
t_RTpor           = r'\*'
t_RTdiv           = r'\/'

t_RTcoma         = r'\,'
t_RTpunto         = r'\.'
t_RTdpuntos       = r'\:'
t_RTptcoma        = r'\;'
t_RTpa            = r'\('
t_RTpc            = r'\)'
t_RTllavea        = r'\{'
t_RTllavec        = r'\}'
t_RTigual         = r'\='

#RTdecimal
def t_RTdecimal(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

#RTnumero
def t_RTnumero(n):
    r'\d+'
    try:
        if(n.value != None):
            n.value = int(n.value)
        else:
            n.value = 'nothing'
    except ValueError:
        print("Valor del RTnumero demasiado grande %d", n.value)
        n.value = 0
    return n

#RTcadena
def t_RTcadena(t):
    r'(\".*?\")'
    t.value = t.value[1:-1] #Se remueven las comillas de la entrada
    t.value = t.value.replace('\\"','\"')
    t.value = t.value.replace("\\'","\'")
    t.value = t.value.replace('\\\\','\\')
    t.value = t.value.replace('\\t', '\t')
    t.value = t.value.replace('\\n', '\n')
    return t

#Identificador

def t_RTid(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'RTid')# Check for reserved words
    return t

#Comentario de Una Linea
def t_Com_Simple(t):
    r'\/\/.*'
    t.lexer.lineno += 1

#Comentario Multilinea
def t_Com_Multiple(t):
    r'\/\*(.|\n)*?\*\/'
    t.lexer.lineno += t.value.count('\n')
    
#Nueva Linea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Caracteres ignorados
t_ignore = " \t"

#Error
def t_error(t):
    t.lexer.skip(1)

def find_column(inp, t):
    line_start = inp.rfind('\n', 0, t.lexpos) + 1
    return (t.lexpos - line_start) + 1

def test_lexer(lexer):
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input

lexer = lex.lex(reflags = re.IGNORECASE)