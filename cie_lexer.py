import re

class Lexer(object):
    def __init__(self, code):
        self.code = re.findall(r'\S+|\n', code)

    def tokenizer(self):
        # Initialize variables
        tokens      = []
        code        = self.code
        code_index  = 0

        # Iterate through the code tokens
        while code_index < len(code):
            word = code[code_index]

            # Create tokens
            if word in ['get', 'set', 'create']:
                if word == 'set':
                    tokens.append(["VARIABLE_DECLARE", word])
                elif word == 'get':
                    tokens.append(["EXISTING_VARIABLE", word])
                elif word == 'create':
                    tokens.append(["VARIABLE_CREATE", word])

            elif word in ['equals', 'plus', 'minus', 'multiplied', 'divided', 'to', 'bigger', 'smaller', 'not']:
                tokens.append(["OPERATOR", word])

            elif word == 'say':
                tokens.append(['SAY', word])

            elif word[0] == '"' and word[len(word) - 1] == '"':
                wordcut = word[1:-1]
                tokens.append(["QUOTES", '"'])
                tokens.append(["IDENTIFIER", wordcut])
                tokens.append(["QUOTES", '"'])

            elif word == 'if':
                tokens.append(["CONDITIONAL", word])

            elif word == 'else':
                tokens.append(["ELSE", word])

            elif word == 'else-if':
                tokens.append(["ELSE_IF", word])

            elif word == 'finished':
                tokens.append(["IF_DONE", word])

            elif word == 'done':
                tokens.append(["LOOP_DONE", word])

            elif word == 'run':
                tokens.append(["FUNCTION_RUN", word])

            elif word == 'comment':
                tokens.append(["COMMENT", word])

            elif word == 'while':
                tokens.append(["WHILE_LOOP", word])

            elif word[0] == '"':
                tokens.append(["QUOTES", '"'])
                try:
                    wordcut = word[1:]
                    if wordcut[0] == '$':
                        tokens.append(["INLINE_VARIABLE", '$'])
                        tokens.append(["IDENTIFIER", wordcut[1:]])
                    else:
                        tokens.append(["IDENTIFIER", wordcut])
                except:
                    pass

            elif word[len(word) - 1] == '"':
                wordcut = word[:-1]
                try:
                    wordcut = word[:-1]
                    if wordcut[0] == '$':
                        tokens.append(["INLINE_VARIABLE", '$'])
                        tokens.append(["IDENTIFIER", wordcut[1:]])
                    else:
                        tokens.append(["IDENTIFIER", wordcut])
                    tokens.append(["QUOTES", '"'])
                except:
                    pass

            elif word == 'use_ui':
                tokens.append(["USE_UI", word])

            elif word == 'ui_text':
                tokens.append(["UI_TEXT", word])

            elif word == 'ui_app_end':
                tokens.append(["UI_END", word])

            elif word == '"':
                tokens.append(["QUOTES", word])

            elif word == 'math':
                tokens.append(["MATH", word])

            elif word == 'then':
                tokens.append(["THEN", word])

            elif word == 'format':
                tokens.append(["FORMAT_STRING", word])

            elif word == "user-input":
                tokens.append(["USER_INPUT", word])

            elif re.match('[0-9]', word):
                tokens.append(["NUMBER", word])

            elif word[0] == '$':
                tokens.append(["INLINE_VARIABLE", '$'])
                wordcut = word[1:]
                if wordcut[len(wordcut) - 1] == '.':
                    tokens.append(["IDENTIFIER", wordcut[:1]])
                else:
                    tokens.append(["IDENTIFIER", wordcut])

            elif re.match('[a-z]', word) or re.match('[A-Z]', word):
                tokens.append(["IDENTIFIER", word])

            elif word in '=+-/*':
                tokens.append(["INVALID_CHARACTER", word])

            elif word == '\n':
                tokens.append(["LINE_ENDING", '.'])

            code_index += 1
        return tokens