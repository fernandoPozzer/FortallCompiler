from parser import parser, memory


file_name = sys.argv[1]

with open(file_name, 'r', encoding='utf-8') as f:
    code = f.read()

parser.parse(code)
# print("x =", memory['x'])  # Deve imprimir x = 3