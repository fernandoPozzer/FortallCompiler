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
    if isinstance(ast, tuple):
        op = ast[0]

        # números
        if op == 'num':
            return ast[1]

        # variáveis (não tratadas aqui)
        elif op == 'var':
            raise ValueError(f"Variável não definida: {ast[1]}")

        # negação
        elif op == 'neg':
            return -avaliar_ast(ast[1])

        # operadores binários
        elif op in ('+', '-', '*', '/'):
            left = avaliar_ast(ast[1])
            right = avaliar_ast(ast[2])
            if op == '+': return left + right
            if op == '-': return left - right
            if op == '*': return left * right
            if op == '/': return left / right

        # valor composto com produto (ex: value_or_prod)
        elif op == 'value_and_prod':
            left = avaliar_ast(ast[1])
            right = avaliar_ast(ast[2])
            return left * right  # sempre multiplicação nesse caso

        else:
            raise ValueError(f"Operação desconhecida: {op}")
    else:
        return ast  # valor literal

    
