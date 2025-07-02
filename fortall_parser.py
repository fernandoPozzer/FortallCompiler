import ply.yacc as yacc
from lexer import tokens

from execute_functions import *

memory = {}

def p_program(p):
    '''first_rule : PROGRAM ID SEMICOLON code_start'''
    p[0] = p[4]

    print(f"\nMEMORIA INICIAL: {memory}")
    print(f"AST: {p[0]}\n\n")
    execute(p[0])
    print(f"\nMEMORIA APOS FIM: {memory}\n")

def p_code_start(p):
    '''code_start : decl code_block PERIOD
                  | code_block PERIOD'''

    # como a decl ja foi feita, nao vai para a AST
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]

#################################
# Declaracao de variaveis
#################################

def p_decl(p):
    '''decl : VAR var_list'''
    pass

def p_var_list(p):
    '''var_list : id_list TYPEDEF VARTYPE SEMICOLON another_var_list'''

    for decl_var in p[1]:
        if p[3] == 'inteiro':
            memory[decl_var] = ['inteiro', 0]
        else: # logico
            memory[decl_var] = ['logico', 0]

    # print(f"declaration: {memory}")

def p_another_var_list(p):
    '''another_var_list : var_list
                        | empty'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = []

#################################
# Bloco de codigo (inicio ... fim)
#################################

def p_code_block(p):
    '''code_block : BEGIN code_block_end'''
    p[0] = ('block', p[2])

def p_code_block_end(p):
    '''code_block_end : cmd_list END'''
    p[0] = p[1]

def p_cmd_list(p):
    '''cmd_list : cond SEMICOLON other_cmds'''
    if p[3] is not None:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_other_cmds(p):
    '''other_cmds : cmd_list
                  | empty'''
    if len(p) == 2:
        if p[1] is None:
            p[0] = []
        else:
            p[0] = p[1]

#################################
# Condicional
#################################

def p_cond(p):
    '''cond : IF bool_expr THEN cond cond_else
            | cmd'''

    if len(p) == 6:
        condition = p[2]
        then_block = p[4]
        else_block = p[5]
        p[0] = ('if', condition, then_block, else_block)
    else:
        p[0] = p[1]

def p_cond_else(p):
    '''cond_else : ELSE cond
                 | empty'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None

#################################
# Comandos
#################################

def p_cmd(p):
    '''cmd : ID ATTR id_value
           | WHILE bool_expr DO cond
           | code_block
           | READ read_list
           | PRINT print_list'''
    
    if len(p) == 2: # code_block
        p[0] = p[1]

    elif len(p) == 3: # read or print
        p[0] = p[2]
    
    elif len(p) == 4: # attr
        p[0] = (p[2], p[1], p[3])

    elif len(p) == 5: # while
        p[0] = ('while', p[2], p[4])

def p_read_list(p):
    '''read_list : LPAREN id_list RPAREN
                 | empty'''
    if len(p) == 4:
        p[0] = ('read', p[2])
    else:
        p[0] = ('read', [])

def p_print_list(p):
    '''print_list : LPAREN elem_print_list RPAREN
                  | empty'''

    if len(p) == 4:
        p[0] = ('print', p[2])
    else:
        p[0] = ('print', [])

def p_elem_print_list(p):
    '''elem_print_list : elem_print other_elem_print'''
    
    p[0] = [p[1]] + p[2]

def p_other_elem_print(p):
    '''other_elem_print : COMMA elem_print_list
                        | empty'''

    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = []

def p_elem_print(p):
    '''elem_print : STRING
                  | math_expr'''

    if isinstance(p[1], str):
        p[0] = ('str', p[1])
    else:
        p[0] = p[1]

#################################
# Expressoes booleanas
#################################

def p_bool_expr(p):
    '''bool_expr : math_expr bool_op'''
    
    if p[2] is None:
        p[0] = p[1]
    else:
        op, right = p[2]
        p[0] = (op, p[1], right)

def p_bool_op(p):
    '''bool_op : EQUALS math_expr
               | DIFF math_expr
               | LT math_expr
               | LEQ math_expr
               | GT math_expr
               | GEQ math_expr
               | empty'''

    if len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = None

#################################
# Expressoes matematicas
#################################

def p_math_expr(p):
    '''math_expr : value_or_prod plus_expr'''
    if p[2] is None:
        p[0] = p[1]
    else:
        if len(p[2]) == 3:
            op, left, right = p[2]
            p[0] = (op, p[1], p[2])
        else:
            op, left = p[2]
            p[0] = (op, p[1], left)

def p_plus_expr(p):
    '''plus_expr : PLUS value_or_prod plus_expr
                 | MINUS value_or_prod plus_expr
                 | empty'''

    if len(p) == 2:
        p[0] = None
    elif p[3] is None:
        p[0] = (p[1], p[2])
    else:
        if len(p[3]) > 2:
            p[0] = (p[1], p[2], p[3])
        else:
            p[0] = (p[1], p[2], p[3][1])
        

def p_value_or_prod(p):
    '''value_or_prod : neg_pos_value prod_expr'''
    if p[2] is None:
        p[0] = p[1]
    else:
        if len(p[2]) == 3:
            op, left, right = p[2]
            p[0] = (op, p[1], p[2])
        else:
            op, left = p[2]
            p[0] = (op, p[1], left)

def p_prod_expr(p):
    '''prod_expr : MULT neg_pos_value prod_expr
                 | DIV neg_pos_value prod_expr
                 | empty'''
    if len(p) == 2:
        p[0] = None
    elif p[3] is None:
        p[0] = (p[1], p[2])
    else:
        if len(p[3]) > 2:
            p[0] = (p[1], p[2], p[3])
        else:
            p[0] = (p[1], p[2], p[3][1])

def p_neg_pos_value(p):
    '''neg_pos_value : MINUS expr_value
                     | expr_value'''
    if len(p) == 3:
        p[0] = ('neg', p[2])
    else:
        p[0] = p[1]

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

def p_id_value(p):
    '''id_value : LOGICVALUE
                | math_expr'''
    if p[1] == 'VERDADEIRO':
        p[0] = 1
    elif p[1] == 'FALSO':
        p[0] = 0
    else:
        p[0] = p[1]

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

parser = yacc.yacc()

def eval_condition(bool_expr):
    if bool_expr[0] == '<':
        return get_value(bool_expr[1]) < get_value(bool_expr[2])

    if bool_expr[0] == '>':
        return get_value(bool_expr[1]) > get_value(bool_expr[2])
    
    if bool_expr[0] == '<>':
        return get_value(bool_expr[1]) != get_value(bool_expr[2])

    if bool_expr[0] == '<=':
        return get_value(bool_expr[1]) <= get_value(bool_expr[2])

    if bool_expr[0] == '>=':
        return get_value(bool_expr[1]) >= get_value(bool_expr[2])

    if bool_expr[0] == '=':
        return get_value(bool_expr[1]) == get_value(bool_expr[2])

    return get_value(bool_expr[1]) != 0

def execute_cmd(cmd):
    op = cmd[0]

    if op == ':=':
        var = cmd[1]

        if var not in memory:
            raise SemanticError(f"Variável {var} não declarada")

        memory[var][1] = get_value(cmd[2])

    elif op == 'if':
        cond = eval_condition(cmd[1])
        if cond:
            execute_cmd(cmd[2])
        elif cmd[3] is not None:
            execute_cmd(cmd[3])

    elif op == 'block':
        for c in cmd[1]:
            execute_cmd(c)

    elif op == 'while':
        cond = eval_condition(cmd[1])
        while cond:
            execute_cmd(cmd[2])
            cond = eval_condition(cmd[1])

    elif op == 'print':
        exec_print(cmd[1])

    elif op == 'read':
        exec_read(cmd[1])

def execute(ast):
    if ast[0] == 'block':
        for cmd in ast[1]:
            execute_cmd(cmd)
    else:
        execute_cmd(ast)