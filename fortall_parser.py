import ply.yacc as yacc
from lexer import tokens

memory = {}

# # Programa é uma lista de comandos
# def p_program(p):
#     '''program : stmt_list'''
#     for stmt in p[1]:
#         execute(stmt)

# def p_stmt_list(p):
#     '''stmt_list : stmt stmt_list
#                  | stmt'''
#     if len(p) == 3:
#         p[0] = [p[1]] + p[2]
#     else:
#         p[0] = [p[1]]

# def p_stmt_assign(p):
#     '''stmt : ID EQUALS expr SEMI'''
#     p[0] = ('assign', p[1], p[3])

# def p_stmt_while(p):
#     '''stmt : WHILE LPAREN condition RPAREN LBRACE stmt_list RBRACE'''
#     p[0] = ('while', p[3], p[6])

# def p_condition(p):
#     '''condition : expr LT expr'''
#     p[0] = ('lt', p[1], p[3])

# def p_expr_plus(p):
#     '''expr : expr PLUS expr'''
#     p[0] = ('plus', p[1], p[3])

# def p_expr_num(p):
#     '''expr : NUM'''
#     p[0] = ('num', p[1])

# def p_expr_var(p):
#     '''expr : ID'''
#     p[0] = ('var', p[1])

def p_program(p):
    '''begin_code : PROGRAM ID SEMICOLON stmt_list'''
    print("BEGIN")
    pass

def p_stmt_list(p):
    '''stmt_list : decl'''
    pass
    
def p_decl(p):
    '''decl : VAR var_list'''
    pass

def p_var_list(p):
    '''var_list : id_list TYPEDEF INT SEMICOLON'''
    print(p[1])

def p_id_list(p):
    '''id_list : ID other_ids'''
    p[0] = [p[1]] + p[2]

def p_other_ids(p):
    '''other_ids : COMMA id_list
                 | empty'''
    if len(p) > 2:
        p[0] = list(p[2])
    else:
        p[0] = list()
    
def p_empty(p):
    '''empty : '''
    pass

def p_error(p):
    print(f"Erro de sintaxe no token '{p.value}' (tipo: {p.type}) na linha {p.lineno}")

def p_print(p):
    '''print_expr : PRINT LPAREN STRING RPAREN SEMICOLON'''
    print(p[3])

parser = yacc.yacc()

def eval_expr(expr):
    if expr[0] == 'num':
        return expr[1]
    elif expr[0] == 'var':
        return memory.get(expr[1], 0)
    elif expr[0] == 'plus':
        return eval_expr(expr[1]) + eval_expr(expr[2])

def eval_condition(cond):
    if cond[0] == 'lt':
        return eval_expr(cond[1]) < eval_expr(cond[2])

def execute(stmt):
    if stmt[0] == 'assign':
        _, var, value_expr = stmt
        memory[var] = eval_expr(value_expr)
    elif stmt[0] == 'while':
        print(f"stmt: {stmt}")
        _, cond, block = stmt
        while eval_condition(cond):
            for s in block:
                execute(s)