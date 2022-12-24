import sys

# Return Types for lex(input)
ID_TOKEN = 0 # The thing returned is an ID token
INT_TOKEN = 1 # The thing returned is an INT token
LEXEME = 2 # The thing returned is a lexeme
ERROR = 3 # An error has been encountered
END_OF_INPUT = 4 # We have reached the end of the input array
STRING_TOKEN = 5

line = 1; # Keeps track of what line we are currently on. Useful for error messages.

# Tokenize INTs
# Assumes the first character on the input is a digit
# A loop is used to represent the loop transition in the
# state transition diagram
def lexInt(input, sign):
    i = 0
    while i < len(input) and input[i].isdigit():
        i = i + 1
    return [[INT_TOKEN, sign*int("".join(input[0:i]))], input[i:]]

# The minus sign can be used stand-alone or as part of
# the "arrow" lexeme. If the next character is '>'
# Then we can transition and accept the arrow
# Otherwise we use the empty transition and accept the '-'
def handleMinus(input):
    if len(input) > 1:
        if input[1] == ">":
            return [[LEXEME, "->"], input[2:]]
        elif input[1].isdigit():
            return lexInt(input[1:], -1)
        else:
            return [[LEXEME, "-"], input[1:]]
    else:
        return [[LEXEME, "-"], input[1:]]

# Helper function
# Specifies what characters are allowed after the start of an id
def isIdChar(c):
    return c == "_" or c.isalpha() or c.isdigit()

# Helper function
# Identifies keywords, returning them as lexemes
# Anything not a keyword gets returned as an ID token
def lookup(lexeme):
    if lexeme == "get" or lexeme == "print" or lexeme == "else" or lexeme == "if" or lexeme == "while" or lexeme == "end" or lexeme == "and" or lexeme == "or" or lexeme == "not":
        return [LEXEME, lexeme]
    else:
        return [ID_TOKEN, lexeme]

# Tokenize IDs and Keywords
# Keywords all follow the same pattern as IDs so our state transition diagram
# just detected the pattern and uses lookup to destringuish between the two.
# We have made the design decision that variables cannot be named the same a keyword
def lexIdOrKeyword(input):
    i = 0
    while i<len(input) and isIdChar(input[i]):
        i = i + 1
    return [lookup("".join(input[0:i])), input[i:]] # Use join to convert array to a string

def handleString(input):
    i = 0
    while i<len(input) and input[i] != '"':
        i = i + 1
    return [[STRING_TOKEN, "".join(input[0:i])], input[i+1:]]

# Represents the Start state
def lex(input):
    global line
    i = 0
    # Eat whitespace
    while i < len(input) and input[i].isspace():
        if input[i] == "\n":
            line = line + 1
        i = i + 1

    # Check if we are at the end of input
    if i >= len(input):
        return [[END_OF_INPUT, ""], input]

    input = input[i:] # Remove the whitespace

    if input[0] == "=":
        # Transition on '='
        # return [[LEXEME, "="], input[1:]]
        if len(input) > 1 and input[1] == "=":
            return [[LEXEME, "=="], input[2:]]
        else:
            return [[LEXEME, "="], input[1:]]
    elif input[0] == ";":
        # Transition on ';'
        return [[LEXEME, ";"], input[1:]]
    elif input[0] == ",":
        # Transition on ','
        return [[LEXEME, ","], input[1:]]
    elif input[0] == "*":
        # Transition on '*'
        return [[LEXEME, "*"], input[1:]]
    elif input[0] == "/":
        # Transition on '/'
        return [[LEXEME, "/"], input[1:]]
    elif input[0] == "%":
        # Transition on '%'
        return [[LEXEME, "%"], input[1:]]
    elif input[0] == "<":
        # Transition on '<'
        # This moves us to a new state, but since it is simple we do all the work here
        if len(input) > 1 and input[1] == "=":
            return [[LEXEME, "<="], input[2:]]
        else:
            return [[LEXEME, "<"], input[1:]]
    elif input[0] == ">":
        # Transition on '>'
        # This moves us to a new state, but since it is simple we do all the work here
        if len(input) > 1 and input[1] == "=":
            return [[LEXEME, ">="], input[2:]]
        else:
            return [[LEXEME, ">"], input[1:]]
    elif input[0] == "!":
        if len(input) > 1 and input[1] == "=":
            return [[LEXEME, "!="], input[2:]]
        else:
            return [[ERROR, "Unexpected character '" + input[0] + "' after '!' on line " + str(line)], input]
    elif input[0] == "-":
        # Transition on '-'
        # return handleMinus(input)
        return [[LEXEME, "-"], input[1:]]
    elif input[0].isdigit():
        # Transition on a digit
        return lexInt(input, 1)
    elif input[0] == "+":
        return [[LEXEME, "+"], input[1:]]
        # # Transition on a '+'
        # # This moves us to a new state, but since it is simple we do all the work here
        # if len(input) > 1 and input[1].isdigit():
        #     return lexInt(input, 1)
        # else:
        #     return [[ERROR, "Expected digit after '+' on line " + str(line)], input]
    elif input[0] == "(":
        return [[LEXEME, "("], input[1:]]
    elif input[0] == ")":
        return [[LEXEME, ")"], input[1:]]
    elif input[0] == "_" or input[0].isalpha():
        # Transition on an underscore or a letter
        return lexIdOrKeyword(input)
    elif input[0] == '"':
        return handleString(input[1:])
    else:
        return [[ERROR, "Unexpected character '" + input[0] + "' on line " + str(line)], input]

def peek(input):
    global line
    lineno = line
    [nextToken, i] = lex(input)
    line = line - (line - lineno)
    return [nextToken, input]


# Read entire std input into an array
# This is done for convenience. Usually, the lexer would read directly from a file
#input = list(sys.stdin.read())
#
## Loop through the lexemes and tokens until an error or end of input happens
#[next, input] = lex(input)
#
#while next[0] != END_OF_INPUT and next[0] != ERROR:
#    print(next)
#    [next, input] = lex(input)
#
#if next[0] == ERROR:
#    print("ERROR: " + next[1])


