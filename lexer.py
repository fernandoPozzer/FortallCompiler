import ply.lex as lex

tokens = (
    'ID',
    'NUM',
    'STRING',

    # operacoes aritmeticas

    'PLUS',
    'MINUS',
    'MULT',
    'DIV',
    'LPAREN',
    'RPAREN',

    # palavras reservadas
    
    'WHILE',
    'DO',
    'BEGIN',
    'END',
    'IF',
    'ELSE',
    'THEN',
    'VAR',
    'PRINT',
    'PROGRAM',
    
    # tipos de variaveis

    'VARTYPE',
    'TYPEDEF',
    'ATTR',

    'LOGICVALUE',

    'LT',
    'LEQ',

    'GT',
    'GEQ',

    'DIFF',
    'EQUALS',
    
    'SEMICOLON',
    'COMMA',
    'PERIOD',
    
)

t_LT        = r'<'
t_LEQ       = r'<='

t_GT        = r'>'
t_GEQ       = r'>='

t_DIFF      = r'<>'
t_EQUALS    = r'='

t_SEMICOLON = r';'
t_TYPEDEF   = r':'
t_ATTR      = r':='
t_COMMA     = r','
t_PERIOD    = r'\.' 

# operacoes aritmeticas

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_MULT    = r'\*'
t_DIV     = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

reserved = {
    'enquanto': 'WHILE',
    'faca'    : 'DO',
    'se'      : 'IF',
    'senao'   : 'ELSE',
    'entao'   : 'THEN',
    'inicio'  : 'BEGIN',
    'fim'     : 'END',
    'var'     : 'VAR',
    'logico'  : 'VARTYPE',
    'inteiro' : 'VARTYPE',
    'escrever': 'PRINT',
    'programa': 'PROGRAM',
    'VERDADEIRO' : 'LOGICVALUE',
    'FALSO' : 'LOGICVALUE',
}

def t_STRING(t):
    r"'[a-zA-Z0-9_ ]*'"
    t.value = t.value[1:-1]
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_error_variable(t):
    r'[0-9]+[a-zA-Z_]+'
    raise LexError(f"É var ou num? {t.value} (linha {t.lineno})")

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_comment(t):
    r'/\*[a-zA-Z0-9_<>= ]*\*/'
    pass

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    raise LexError(f"Caractere alienígena: {t.value[0]} (linha {t.lineno})")

lexer = lex.lex()

class LexError(Exception):
    pass

def check_for_lex_errors(code):
    
    lexer.input(code)

    while True:
        try:
            tok = lexer.token()
        except LexError as lex_error:
            print(f"\nLEX ERROR: {lex_error}\n")
            return True

        if not tok:
            return False