import sys

file_name = sys.argv[1]

with open(file_name, 'r', encoding='utf-8') as f:
    code = f.read()

from lexer import lexer, LexError

lexer.input(code)

cur_line = -1
while True:
    try:
        tok = lexer.token()
    except LexError as l:
        print(f"\n\nLEX ERROR: {l}")
        break

    if not tok:
        break

    if tok.lineno != cur_line:
        cur_line = tok.lineno
        print(f"\nLine {cur_line}:  ", end = " ")
    
    if tok.type == "NUM" or tok.type == "ID":
        print(f"({tok.type}, {tok.value})", end = " ")
    else:
        print(f"{tok.type}", end = " ")

print("\n")