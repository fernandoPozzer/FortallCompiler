from fortall_parser import parser, memory
from lexer import check_for_lex_errors

import sys

file_name = sys.argv[1]

with open(file_name, 'r', encoding='utf-8') as f:
    code = f.read()

if not check_for_lex_errors(code):
    parser.parse(code)

# print("x =", memory['x'])  # Deve imprimir x = 3