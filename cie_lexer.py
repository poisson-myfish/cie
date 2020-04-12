import re

class Lexer(object):
    def __init__(self, code):
        self.code = code

    def tokenizer(self):
        # Initialize variables
        tokens      = []
        code        = self.code.split()
        code_index  = 0

        # Iterate through the code tokens
        while code_index < len(code):
            word = code[code_index]

            # Create tokens
            if word in 'existing-variable':
                if word == 'variable':
                    tokens.append(["VARIABLE_DECLARE", word])
                elif word == 'existing-variable':
                    tokens.append(["EXISTING_VARIABLE", word])

            elif word in 'equals/plus/minus/multiplied/divided':
                tokens.append(["OPERATOR", word])

            elif word == 'say':
                tokens.append(['SAY', word])

            elif re.match('[0-9]', word):
                tokens.append(["NUMBER", word])

            elif word in ["'", '"']:
                tokens.append(["QUOTES", word])

            elif re.match('[a-z]', word) or re.match('[A-Z]', word):
                tokens.append(["IDENTIFIER", word])

            elif word in '=+-/*':
                tokens.append(["INVALID_CHARACTER", word])

            elif word == '.':
                tokens.append(["LINE_ENDING", '.'])

            code_index += 1

        return tokens