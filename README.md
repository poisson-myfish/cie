# cie
CIE (Code in English) is a programming language that aims to be as close to english as possible.

`set name equals "Bob"`

`say get name`

# Installation
1. Install Python 3.6 or later
2. Clone the repo or download as ZIP
3. Code!

## Running code
To run code, you have to create a file with the .cie extension, and pass it as an argument to the python program. For example, if you have a `main.cie` file, to run it do:

    $ python main.py main.cie

Now, go see the "A HelloWorld Program" section!

## Notes:
1. At the end of every CIE program, you have to have a blank line, otherwise the last line of your program will not run.

2. See issue #1


## A HelloWorld Program
    say "Hello, World!"

It's easy, isn't it?


# Documentation

## say
Say is a function that is used to print something to the screen.

**Usage: say "<my_string>"**

## set 
Set is a function that is used to assign a value to a variable.

**Usage: set <variable_name> to <variable_value>**

## get
Get is a function that is used to get the value of a variable. It is used in combination with:
* say
* if conditionals
* else-if conditionals
* ui_text

**Usage: say get <variable_name>**

## create
Create is a function that is used to create an empty variable. Note: It is not required for creating variables, as `set` creates them automatically.

**Usage: create <variable_name>**

## plus / minus / multiplied / divided
These operators are used inside **math** blocks.

**Usage: math "1 plus 1"**

## to
This operator is used to assign a value to a variable. See `set`.

**Usage: set <variable_name> to <variable_value>**

## bigger / smaller / equals
These operators are used in if and if-else conditionals to compare two values.

**Usage: if get <variable_one> equals get <variable_two> then...**

**Note: See issue #1**

## if / else / else-if / done
These conditionals are used to run some lines of code only if a condition is met.

**Usage:**

    if <variable_one> equals <variable_two> then
        say "Hello"
    else-if <variable_one> bigger <variable_two> then
        say "Goodbye"
    else
        say "Nothing"
    done


**Note: See issue #1**


## run
This function is used to run actions. See **actions** for more details.

**Usage: run say_my_name**

## comment
This is used to comment a block of code you don't want the interpreter to run.

**Usage: comment This has to be fixed**

## UI
### use_ui
This function is used to initialize the UI Window. It is required to make UI, and it has to be placed before any other UI components.

**Usage: use_ui**

### ui_text
This function adds a label to the UI Window.

**Usage: ui_text YourTextWithoutSpaces**

or

**Usage: ui_text get <variable_name>**

### ui_app_end
This function is used to define the ending of your UI app. It is required for the Window to even appear.

**Usage: ui_app_end**


## math
This function is used to calculate any value, and variables can be put inside it by preceding them with the `$` symbol.

**Usage: math "1 plus $your_variable_name"**

It is used with the `set` function.

## format
This function is used to insert variables into strings of text. It is used with `say`.

**Usage: say format "It's a nice day. Am I right, $variable_name?"**

## user-input
This function is used to take input from the user. It is used with `set`.

**Usage: set name to user-input**

## Actions
Actions are like functions in other programming languages. Each action has a different file with the .cie extension.

**Example:**

For a file called **say_my_name.cie**, in another file is is runned like this:

    run say_my_name

Notice that you don't need the extension to run actions, it is added automatically. Just be sure to have the .cie extension on your action filename.

