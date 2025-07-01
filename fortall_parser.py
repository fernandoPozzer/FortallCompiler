import ply.yacc as yacc
from lexer import tokens

from execute_functions import *

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
    '''cond_else : ELSE cond
                 | empty'''
    pass

#################################
# Comandos
#################################

def p_cmd(p):
    '''cmd : ID ATTR id_value
           | WHILE bool_expr DO cond
           | code_block
           | READ read_list
           | PRINT print_list'''
    # for i in p:
    #     print(i, end='')
    # print()
    pass

def p_read_list(p):
    '''read_list : LPAREN id_list RPAREN
                 | empty'''
    pass

def p_print_list(p):
    '''print_list : LPAREN elem_print_list RPAREN
                  | empty'''
    pass

def p_elem_print_list(p):
    '''elem_print_list : elem_print other_elem_print'''
    pass

def p_other_elem_print(p):
    '''other_elem_print : COMMA elem_print_list
                        | empty'''
    pass

def p_elem_print(p):
    '''elem_print : STRING
                  | math_expr'''
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
    '''math_expr : value_or_prod plus_expr'''
    
    if p[2] is None:
        p[0] = p[1]
    else:
        # plus_expr já é uma AST com '+' ou '-' como raiz
        # precisamos inserir p[1] como o operando esquerdo mais à esquerda

        # Exemplo: p[1] = a, p[2] = ('+', b, c)
        op = p[2][0]

        if len(p[2]) == 2:
            # ('+', b) → vira ('+', a, b)
            p[0] = (op, p[1], p[2][1])
        else:
            # ('+', b, c) → encadeia: (op, a, subtree)
            p[0] = (op, p[1], p[2][2])  # p[2][1] já está em p[1]
            atual = p[0]
            for i in range(3, len(p[2])):
                atual = (p[2][i - 2], atual, p[2][i])
            p[0] = atual

    print(f"math_expr: {p[0]}")
    print(f"RESULTADO: {avaliar_ast(p[0])}")

def p_plus_expr(p):
    '''plus_expr : PLUS value_or_prod plus_expr
                 | MINUS value_or_prod plus_expr
                 | empty'''

    if len(p) == 4:
        op = '+' if p[1] == '+' else '-'
        left = p[2]
        right = p[3]

        if right is None:
            p[0] = (op, left)
        else:
            p[0] = (op, left, right)
    else:
        p[0] = None

def p_value_or_prod(p):
    '''value_or_prod : neg_pos_value prod_expr'''

    if p[2] is None:
        p[0] = p[1]
    else:
        # prod_expr é uma cadeia como: ('*', b, ('/', c))
        # Devemos aplicar p[1] como "esquerda" da primeira operação
        op, *rest = p[2]

        # Se prod_expr tem só dois elementos: ('*', b)
        if len(rest) == 1:
            p[0] = (op, p[1], rest[0])
        else:
            # é do tipo ('*', b, outra coisa)
            p[0] = (op, p[1], rest[0])
            atual = p[0]
            for i in range(1, len(rest), 2):
                atual = (rest[i-1], atual, rest[i])
            p[0] = atual

def p_prod_expr(p):
    '''prod_expr : MULT neg_pos_value prod_expr
                 | DIV neg_pos_value prod_expr
                 | empty'''

    if len(p) == 4:
        op = '*' if p[1] == '*' else '/'
        left = p[2]
        right = p[3]

        if right is None:
            p[0] = (op, left)
        else:
            p[0] = (op, left, right)
    else:
        p[0] = None

def p_neg_pos_value(p):
    '''neg_pos_value : MINUS expr_value
                     | expr_value'''
    if len(p) == 3:
        p[0] = ('neg', p[2])
    else:
        p[0] = p[1]
    
    # print(f"neg_pos_value: {p[0]}")

def p_expr_value(p):
    '''expr_value : LPAREN math_expr RPAREN
                  | ID
                  | NUM'''
    if len(p) == 4:
        p[0] = p[2]
    elif isinstance(p[1], str):
        p[0] = ('id', p[1])
    else:
        p[0] = ('num', p[1])

    # print(f"expr_value: {p[0]}")

def p_id_value(p):
    '''id_value : LOGICVALUE
                | math_expr'''
    if p[1] == 'VERDADEIRO':
        p[0] = ('logic', 1)
    elif p[1] == 'FALSO':
        p[0] = ('logic', 0)
    else:
        p[0] = ('math_expr', p[1])

    # print(f"id_value: {p[0]}")

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

# def p_print(p):
#     '''print_expr : PRINT LPAREN STRING RPAREN SEMICOLON'''
#     print(p[3])

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