# FortallCompiler

## Rodando o trabalho

Este trabalho usa o pacote `ply` (python-lex-yacc), o qual pode ser instalado com o seguinte comando: `pip install ply`.

Para rodar o interpretador, deve-se usar o seguinte comando: `python main.py <nome_do_codigo>.txt`. Tem alguns exemplos disponíveis, como `math.txt`, que realiza operações matemáticas e printa elas com seu gabarito.

## Gramática

Foi implementada toda a gramática apresentada no documento do Fortall. Além disso, também é possível fazer comentários usando `/**/`.

## Analizador Léxico

Dois tipos de erros são mostrados:
 - caractere alienígena (caractere que não pertence à linguagem);
 - var ou num? (quando uma palavra inicia com número seguido de letras).

Pode-se rodar o `lex_debugger` da mesma forma que se roda a `main` para obter apenas os tokens do código.

## Analizador Sintático

Pelas regras de produção, o yacc interno do ply consegue apontar erros de sintaxe.

## Analizador Semântico

Para a parte semântica, o trabalho aponta quando uma variável é usada sem ter sido declarada.

Deve-se notar que, como na linguagem C booleanos e ints podem ser operados entre si, o presente trabalho não aponta erros de "tipo errado de variável". Apesar disso, no dictionary `memory`, onde são guardadas as variáveis, existe uma distinção entre inteiro e lógicos.
