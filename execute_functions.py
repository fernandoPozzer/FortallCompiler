def imprime_ast(ast, nivel=0):
    indent = '  ' * nivel  # 2 espaços por nível
    
    if isinstance(ast, tuple):
        print(f"{indent}('{ast[0]}',")
        for filho in ast[1:]:
            imprime_ast(filho, nivel + 1)
        print(f"{indent})")
    else:
        print(f"{indent}{repr(ast)}")

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
    print("\n\nFORTALL-PRINT: ", end='')
    for part in p:
        if part[0] == 'str':
            print(part[1], end='')
        else:
            # print(part)
            print(avaliar_ast(part), end='')
            # pass

    print("")

class SemanticError(Exception):
    pass

    
