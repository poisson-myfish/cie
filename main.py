from cie_lexer  import Lexer
from cie_parser import Parser
import re

def main():
    content = ''

    with open('test.cie', 'r') as file:
        content = file.read()

    # Call the lexer
    lex     = Lexer(content)
    tokens  = lex.tokenizer()

    # Call the parser
    parse = Parser(tokens)
    parse.parse()

if __name__ == '__main__':
    main()