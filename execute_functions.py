
def avaliar_ast(ast):
    from fortall_parser import memory

    if isinstance(ast, tuple):
        op = ast[0]

        if op == 'num':
            return ast[1]

        elif op == 'id':
            if ast[1] not in memory: # var nao declarada
                raise SemanticError(f"variável {ast[1]} não foi previamente declarada.")
            
            return memory[ast[1]][1]

        elif op == 'neg':
            return -avaliar_ast(ast[1])

        elif op in ('+', '-', '*', '/'):
            left = avaliar_ast(ast[1])
            right = avaliar_ast(ast[2])
            if op == '+': return left + right
            if op == '-': return left - right
            if op == '*': return left * right
            if op == '/': return int(left / right)

        # valor composto com produto (ex: value_or_prod)
        elif op == 'value_and_prod':
            left = avaliar_ast(ast[1])
            right = avaliar_ast(ast[2])
            return left * right  # sempre multiplicação nesse caso

        else:
            raise ValueError(f"Operação desconhecida: {op}")
    else:
        return ast

def exec_print(p):
    for part in p:
        if part[0] == 'str':
            print(part[1], end='')
        else:
            # print(part)
            print(avaliar_ast(part), end='')

    print("")

def exec_read(p):
    from fortall_parser import memory

    for i in range(len(p)):
        read_value = int(input())

        var = p[i]

        if var not in memory:
            raise SemanticError(f"Variável {var} não declarada")

        memory[var] = read_value

def execute_code(p):
    pass

class SemanticError(Exception):
    pass

    
