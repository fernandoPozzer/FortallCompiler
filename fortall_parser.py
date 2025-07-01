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
    '''first_rule : PROGRAM ID SEMICOLON code_start'''
    pass

def p_stmt_list(p):
    '''code_start : decl code_block PERIOD
                  | code_block PERIOD'''
    pass

#################################
# Declaracao de variaveis
#################################

def p_decl(p):
    '''decl : VAR var_list'''
    pass

def p_var_list(p):
    '''var_list : id_list TYPEDEF VARTYPE SEMICOLON another_var_list'''
    # print(p[1])

    for decl_var in p[1]:
        if p[3] == 'inteiro':
            memory[decl_var] = ['inteiro', 0]
        else: # logico
            memory[decl_var] = ['logico', 0]

def p_another_var_list(p):
    '''another_var_list : var_list
                        | empty'''
    pass

#################################
# Bloco de codigo (inicio ... fim)
#################################

def p_code_block(p):
    '''code_block : BEGIN code_block_end'''
    pass

def p_code_block_end(p):
    '''code_block_end : cmd_list END'''
    pass

def p_cmd_list(p):
    '''cmd_list : cond SEMICOLON other_cmds'''
    pass

def p_other_cmds(p):
    '''other_cmds : cmd_list
                  | empty'''
    pass

#################################
# Condicional
#################################

def p_cond(p):
    '''cond : IF bool_expr THEN cond cond_else
            | cmd'''
    pass

def p_cond_else(p):
    '''cond_else : cond
                 | empty'''
    pass

#################################
# Comandos
#################################

def p_cmd(p):
    '''cmd : ID ATTR id_value'''
    pass

def p_bool_expr(p):
    '''bool_expr : math_expr bool_op'''
    pass

def p_bool_op(p):
    '''bool_op : EQUALS math_expr
               | DIFF math_expr
               | LT math_expr
               | LEQ math_expr
               | GT math_expr
               | GEQ math_expr
               | empty'''
    pass

def p_math_expr(p):
    '''math_expr : ID'''
    pass

def p_id_value(p):
    '''id_value : LOGICVALUE'''
    pass

#################################
# Lista de Variaveis
#################################

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
# print(memory['a'])

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