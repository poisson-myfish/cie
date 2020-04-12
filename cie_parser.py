from cie_errors import ErrorAndQuit, DebugMessage

class Parser(object):
    def __init__(self, tokens):
        self.tokens         = tokens
        self.token_index    = 0
        self.variables      = {}

    def parse(self):
        while self.token_index < len(self.tokens):
            token_type  = self.tokens[self.token_index][0]
            token_value = self.tokens[self.token_index][1]

            if token_type == "VARIABLE_DECLARE" and token_value == 'variable':
                self.parse_variable_declare(self.tokens[self.token_index:len(self.tokens)])
            
            elif token_type == "SAY":
                self.parse_say(self.tokens[self.token_index:len(self.tokens)])

            self.token_index += 1


    def parse_variable_declare(self, token_stream):
        tokens_checked  = 0
        variable_name   = ''
        variable_value  = ''
        string_started  = False

        for token in range(0, len(token_stream)):
            token_type  = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token_type == "LINE_ENDING":
                self.variables[variable_name] = variable_value
                break

            elif token == 1 and token_type == "IDENTIFIER":
                variable_name = token_value
            elif token == 1 and token_type != "IDENTIFIER":
                ErrorAndQuit(f'Variable name "{token_value}" is illegal')

            elif token == 2 and token_type != "OPERATOR":
                ErrorAndQuit(f'{token_value} is not an operator')

            elif token == 3 and token_type == "QUOTES":
                string_started = True

            elif token == 3 and token_type == "NUMBER":
                variable_value = token_value

            elif string_started == True:
                if token_type != "QUOTES":
                    variable_value += token_value + " "
                else:
                    string_started = False


            tokens_checked += 1

        self.token_index += tokens_checked


    def parse_say(self, token_stream):
        tokens_checked  = 0
        variable_name  = ''
        say_what        = ''

        for token in range(0, len(token_stream)):
            token_type  = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token_type == "LINE_ENDING":
                print(self.variables[variable_name])
                break
            
            elif token == 1 and token_type == "EXISTING_VARIABLE":
                say_what = 'variable'

            elif token == 2 and token_type in ["STRING", "NUMBER", "IDENTIFIER"]:
                variable_name = token_value

            tokens_checked+= 1

        self.token_index += tokens_checked

            