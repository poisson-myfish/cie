from cie_errors import ErrorAndQuit, DebugMessage, InternalError
from cie_lexer  import Lexer
from tkinter import *

class Parser(object):
    def __init__(self, tokens):
        self.tokens             = tokens
        self.token_index        = 0
        self.variables          = {}
        self.conditional_true   = True

    def parse(self):
        while self.token_index < len(self.tokens):
            token_type  = self.tokens[self.token_index][0]
            token_value = self.tokens[self.token_index][1]
            if self.conditional_true:

                if token_type == "COMMENT":
                    pass

                elif token_type == "USE_UI":
                    self.ui_root = Tk()

                elif token_type == "UI_TEXT":
                    self.parse_ui_text(self.tokens[self.token_index:len(self.tokens)])

                elif token_type == "UI_END":
                    self.parse_ui_end(self.tokens[self.token_index:len(self.tokens)])

                elif token_type == "VARIABLE_DECLARE" and token_value == 'set':
                    self.parse_variable_declare(self.tokens[self.token_index:len(self.tokens)])
                
                elif token_type == "SAY":
                    self.parse_say(self.tokens[self.token_index:len(self.tokens)])

                elif token_type == "VARIABLE_CREATE":
                    self.parse_create_variable(self.tokens[self.token_index:len(self.tokens)])

                elif token_type == "CONDITIONAL":
                    self.parse_conditional(self.tokens[self.token_index:len(self.tokens)])

                elif token_type == "ELSE":
                    self.conditional_true = False

                elif token_type == "ELSE_IF":
                    self.parse_conditional_elseif(self.tokens[self.token_index:len(self.tokens)])

                elif token_type == 'FUNCTION_RUN':
                    self.parse_function_run(self.tokens[self.token_index:len(self.tokens)])


            elif token_type == "ELSE_IF":
                    self.parse_conditional_elseif(self.tokens[self.token_index:len(self.tokens)])

            elif token_type == "ELSE":
                self.conditional_true = True

            elif token_type == "IF_DONE":
                self.conditional_true = True

            elif token_type in ["IF_EQUAL", "IF_NOT_EQUAL", "IF_BIGGER", "IF_SMALLER"]:
                ErrorAndQuit('If conditionals were removed due to various errors. If you want to contribute to fixing them, go to https://github.com/poisson-myfish/cie.')


            self.token_index += 1


    def parse_variable_declare(self, token_stream):
        tokens_checked          = 0
        variable_name           = ''
        variable_value          = ''
        string_started          = False
        math_started            = False
        is_math                 = False
        math_result             = 0
        math_calculation        = ''
        inline_variable_next    = False

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
                ErrorAndQuit(f'"{ token_value }" is not a declaring operator')

            elif token == 2 and token_value != 'to':
                ErrorAndQuit(f'"{ token_value }" is not a declaring operator')

            elif token == 3 and token_type == "QUOTES":
                string_started = True

            elif token == 3 and token_type == "NUMBER":
                variable_value = token_value

            elif string_started:
                if token_type != "QUOTES":
                    variable_value += token_value + " "
                else:
                    string_started = False

            elif token == 3 and token_type == "MATH":
                is_math = True

            elif token == 4 and token_type == "QUOTES" and is_math:
                math_started = True

            elif math_started and is_math and inline_variable_next:
                math_calculation += self.variables[token_value] + ' '
                inline_variable_next = False

            elif math_started and is_math:
                if token_type != "QUOTES":
                    if token_type != "INLINE_VARIABLE":
                        if token_type == "OPERATOR":
                            if token_value == 'plus':
                                math_calculation += ' + '
                            elif token_value == 'minus':
                                math_calculation += ' - '
                            elif token_value == 'multiplied':
                                math_calculation += ' * '
                            elif token_value == 'divided':
                                math_calculation += ' / '
                        elif token_type == "IDENTIFIER":
                            try:
                                math_calculation += token_value
                            except:
                                ErrorAndQuit(f'Illegal character "{ token_value }" in math')
                        else:
                            ErrorAndQuit(f'Illegal character "{ token_value }" in math')
                    else:
                        inline_variable_next = True
                else:
                    math_started = False
                    math_result     = eval(math_calculation)
                    variable_value  = str(math_result)

            elif token == 3 and token_type == "USER_INPUT":
                variable_value = input('')


            tokens_checked += 1

        self.token_index += tokens_checked


    def parse_say(self, token_stream):
        tokens_checked          = 0
        variable_name           = ''
        say_what                = 'none'
        string_value            = ''
        string_started          = False
        string_ended            = False
        inline_variable_next    = False
        variable_said           = False

        for token in range(0, len(token_stream)):
            token_type  = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token_type == "LINE_ENDING" and string_started == False:
                if say_what == 'variable':
                    try:
                        print(self.variables[variable_name])
                    except:
                        ErrorAndQuit(f'Variable "{variable_name}" referenced before assignment')
                elif say_what == 'string' and string_ended:
                    print(string_value)
                elif say_what == 'formatted-string' and string_ended:
                    print(string_value)
                break
            
            elif token == 1 and token_type == "EXISTING_VARIABLE":
                say_what = 'variable'
            elif token == 1 and token_type == "QUOTES":
                say_what        = 'string'
                string_started  = True
            elif token == 1 and token_type == "FORMAT_STRING":
                say_what        = 'formatted-string'
                string_started  = True

            elif token == 2 and token_type in ["STRING", "NUMBER", "IDENTIFIER"] and say_what == 'variable':
                variable_name = token_value
                variable_said = True

            elif token == 2 and say_what == 'formatted-string':
                if token_type == "QUOTES":
                    string_started = True
            
            elif say_what == 'string' and string_started and string_ended == False:
                if token_type != "QUOTES":
                    string_value += token_value + ' '
                else:
                    string_started = False
                    string_ended = True

            elif say_what == 'formatted-string' and string_started and string_ended == False and inline_variable_next:
                string_value += self.variables[token_value] + ' '
                inline_variable_next = False

            elif say_what == 'formatted-string' and string_started and string_ended == False:
                if token_type != "QUOTES":
                    if token_type == "INLINE_VARIABLE":
                        inline_variable_next = True
                    else:
                        string_value += token_value + ' '
                else:
                    string_started = False
                    string_ended = True

            tokens_checked+= 1

        self.token_index += tokens_checked


    def parse_create_variable(self, token_stream):
        tokens_checked  = 0
        variable_name   = ''

        for token in range(0, len(token_stream)):
            token_type          = token_stream[tokens_checked][0]
            token_value         = token_stream[tokens_checked][1]

            if token_type == "LINE_ENDING":
                self.variables[variable_name] = ''
                break
            
            if token == 1 and token_type != "IDENTIFIER":
                ErrorAndQuit(f'Variable name "{ token_value }" is illegal')

            elif token == 1 and token_type == "IDENTIFIER":
                variable_name = token_value

            tokens_checked += 1

        self.token_index += tokens_checked
            

    def parse_conditional(self, token_stream):
        tokens_checked          = 0
        check_ended             = False
        next_variable           = False
        first_variable_name     = ''
        second_variable_name    = ''
        check_type              = ''
        after_token_add         = 0

        for token in range(0, len(token_stream)):
            token_type          = token_stream[tokens_checked][0]
            token_value         = token_stream[tokens_checked][1]

            if token_type == "LINE_ENDING":
                break

            if token == 1 and token_type == "EXISTING_VARIABLE":
                next_variable = True

            elif token == 2 and next_variable and token_type == "IDENTIFIER":
                first_variable_name = token_value
                next_variable = False

            elif token == 3 and token_type == "OPERATOR":
                if token_value == 'equals':
                    check_type = 'equality'
                elif token_value == 'bigger':
                    check_type = 'bigger'
                elif token_value == 'smaller':
                    check_type = 'smaller'
                elif token_value == 'not':
                    check_type == 'not'
                else:
                    ErrorAndQuit(f'"{ token_value }" is not a valid operator for conditionals')
            elif token == 3 and token_type != "OPERATOR":
                ErrorAndQuit(f'"{ token_value }" is not a valid operator for conditionals')

            elif token == 4 and token_type == "EXISTING_VARIABLE":
                next_variable   = True
                after_token_add = 1

            elif token == 4 + after_token_add and token_type == "IDENTIFIER":
                second_variable_name = token_value
                next_variable = False

            elif token == 4 + after_token_add and token_type != "IDENTIFIER":
                ErrorAndQuit(f'"{ token_value }" variable name is illegal')

            elif token == 5 + after_token_add and token_type == "THEN":
                check_ended = True
                if check_ended == True:
                    if check_type == 'equality':
                        try:
                            if self.variables[first_variable_name] == self.variables[second_variable_name]:
                                self.conditional_true = True
                            else:
                                self.conditional_true = False
                        except:
                            ErrorAndQuit(f'Variable "{ first_variable_name }" or "{ second_variable_name }" refereced before assignment')

                    elif check_type == 'bigger':
                        try:
                            if self.variables[first_variable_name] > self.variables[second_variable_name]:
                                self.conditional_true = True
                            else:
                                self.conditional_true = False
                        except:
                            ErrorAndQuit(f'Variable "{ first_variable_name }" or "{ second_variable_name }" refereced before assignment')

                    elif check_type == 'smaller':
                        try:
                            if self.variables[first_variable_name] < self.variables[second_variable_name]:
                                self.conditional_true = True
                            else:
                                self.conditional_true = False
                        except:
                            ErrorAndQuit(f'Variable "{ first_variable_name }" or "{ second_variable_name }" refereced before assignment')

                    elif check_type == 'not':
                        try:
                            if self.variables[first_variable_name] != self.variables[second_variable_name]:
                                self.conditional_true = True
                            else:
                                self.conditional_true = False
                        except:
                            ErrorAndQuit(f'Variable "{ first_variable_name }" or "{ second_variable_name }" refereced before assignment')

            tokens_checked += 1

        self.token_index += tokens_checked


    def parse_conditional_elseif(self, token_stream):
        tokens_checked          = 0
        check_ended             = False
        next_variable           = False
        first_variable_name     = ''
        second_variable_name    = ''
        check_type              = ''
        after_token_add         = 0

        for token in range(0, len(token_stream)):
            token_type          = token_stream[tokens_checked][0]
            token_value         = token_stream[tokens_checked][1]

            if token_type == "LINE_ENDING":
                break

            if token == 1 and token_type == "EXISTING_VARIABLE":
                next_variable = True

            elif token == 2 and next_variable and token_type == "IDENTIFIER":
                first_variable_name = token_value
                next_variable = False

            elif token == 3 and token_type == "OPERATOR":
                if token_value == 'equals':
                    check_type = 'equality'
                elif token_value == 'bigger':
                    check_type = 'bigger'
                elif token_value == 'smaller':
                    check_type = 'smaller'
                elif token_value == 'not':
                    check_type == 'not'
                else:
                    ErrorAndQuit(f'"{ token_value }" is not a valid operator for conditionals')
            elif token == 3 and token_type != "OPERATOR":
                ErrorAndQuit(f'"{ token_value }" is not a valid operator for conditionals')

            elif token == 4 and token_type == "EXISTING_VARIABLE":
                next_variable   = True
                after_token_add = 1

            elif token == 4 + after_token_add and token_type == "IDENTIFIER":
                second_variable_name = token_value
                next_variable = False

            elif token == 4 + after_token_add and token_type != "IDENTIFIER":
                ErrorAndQuit(f'"{ token_value }" variable name is illegal')

            elif token == 5 + after_token_add and token_type == "THEN":
                check_ended = True
                if check_ended == True:
                    if check_type == 'equality':
                        try:
                            if self.variables[first_variable_name] == self.variables[second_variable_name]:
                                self.conditional_true = not self.conditional_true * -1
                            else:
                                self.conditional_true = False
                        except:
                            ErrorAndQuit(f'Variable "{ first_variable_name }" or "{ second_variable_name }" refereced before assignment')

                    elif check_type == 'bigger':
                        try:
                            if self.variables[first_variable_name] > self.variables[second_variable_name]:
                                self.conditional_true = not self.conditional_true
                            else:
                                self.conditional_true = False
                        except:
                            ErrorAndQuit(f'Variable "{ first_variable_name }" or "{ second_variable_name }" refereced before assignment')

                    elif check_type == 'smaller':
                        try:
                            if self.variables[first_variable_name] < self.variables[second_variable_name]:
                                self.conditional_true = not self.conditional_true * -1
                            else:
                                self.conditional_true = False
                        except:
                            ErrorAndQuit(f'Variable "{ first_variable_name }" or "{ second_variable_name }" refereced before assignment')

                    elif check_type == 'not':
                        try:
                            if self.variables[first_variable_name] != self.variables[second_variable_name]:
                                self.conditional_true = not self.conditional_true * -1
                            else:
                                self.conditional_true = False
                        except:
                            ErrorAndQuit(f'Variable "{ first_variable_name }" or "{ second_variable_name }" refereced before assignment')

            tokens_checked += 1

        self.token_index += tokens_checked


    def parse_function_run(self, token_stream):
        tokens_checked          = 0
        function_token_index    = 1
        function_name           = ''
        function_tokens         = []
        function_content        = ''

        for token in range(0, len(token_stream)):
            token_type          = token_stream[tokens_checked][0]
            token_value         = token_stream[tokens_checked][1]

            if token == 1 and token_type in ["IDENTIFIER", "STRING"]:
                function_name = token_value
                with open(f'{function_name}.cie', 'r') as file:
                    function_content = file.read()
                lex              = Lexer(function_content)
                function_tokens  = lex.tokenizer()
                self.token_index += tokens_checked
                # self.tokens.insert()
                for token in function_tokens:
                    self.tokens.insert(self.token_index + function_token_index, token)
                    function_token_index += 1

            elif token == 1 and token_type not in ["IDENTIFIER", "STRING"]:
                ErrorAndQuit(f'Illegal action name "{token_value}"')

            elif token_type == "LINE_ENDING":
                return

            tokens_checked += 1


    def parse_ui_text(self, token_stream):
        tokens_checked          = 0
        next_variable           = False
        label                   = ''

        for token in range(0, len(token_stream)):
            token_type          = token_stream[tokens_checked][0]
            token_value         = token_stream[tokens_checked][1]

            if token == 1 and token_type in ["IDENTIFIER", "STRING", "NUMBER"]:
                Label(self.ui_root, text=token_value).pack()
            elif token == 1 and token_type == "EXISTING_VARIABLE":
                next_variable = True

            elif token == 2 and token_type == "IDENTIFIER" and next_variable:
                label = self.variables[token_value]
                Label(self.ui_root, text=label).pack()

            elif token_type == "LINE_ENDING":
                return

            tokens_checked += 1


    def parse_ui_end(self, token_stream):
        tokens_checked          = 0

        for token in range(0, len(token_stream)):
            token_type          = token_stream[tokens_checked][0]
            token_value         = token_stream[tokens_checked][1]

            self.ui_root.mainloop()

            tokens_checked += 1