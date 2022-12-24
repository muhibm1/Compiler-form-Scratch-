import lexer
import sys

class Scope:
    def __init__(self, parent):
        self.parent = parent
        self.commandsList = []
    
    def getCommandsList(self):
        return self.commandsList

    def getParent(self):
        return self.parent

    def addCommand(self, command):
        self.commandsList.append(command)

mainScope = Scope(None)

symtab = {}

def parseError(msg):
    print("Parse Error: " + msg + " at line " + str(lexer.line))
    exit()

def lex():
    global nextToken
    global input
    [nextToken, input] = lexer.lex(input)
    # print(nextToken)

def peek(lexeme):
    global nextToken
    global input
    [nextToken, input] = lexer.peek(input)
    if lexeme == nextToken[1]:
        return True
    return False

def peekID():
    global nextToken
    global input
    [nextToken, input] = lexer.peek(input)
    if nextToken[0] == lexer.ID_TOKEN:
        return True
    return False

def peekNUM():
    global nextToken
    global input
    [nextToken, input] = lexer.peek(input)
    if nextToken[0] == lexer.INT_TOKEN:
        return True
    return False

def peekSTR():
    global nextToken
    global input
    [nextToken, input] = lexer.peek(input)
    if nextToken[0] == lexer.STRING_TOKEN:
        return True
    return False

def expect(lexeme):
    lex()
    if nextToken[0] == lexer.END_OF_INPUT:
        parseError("Expected " + lexeme + " but got END OF FILE")
    if not nextToken[1] == lexeme:
        parseError("Expected " + lexeme + " but got "+ nextToken[1])

def expectID():
    lex()
    if nextToken[0] == lexer.END_OF_INPUT:
        parseError("Expected Identifier but got END OF FILE")
    if not nextToken[0] == lexer.ID_TOKEN:
        parseError("Expected Identifier "+" but got "+ nextToken[1])
    else: 
        return nextToken

def expectNUM():
    lex()
    if nextToken[0] == lexer.END_OF_INPUT:
        parseError("Expected Number but got END OF FILE")
    if not nextToken[0] == lexer.INT_TOKEN:
        parseError("Expected Number "+" but got "+ nextToken[1])
    else: 
        return nextToken

def expectSTR():
    lex()
    if nextToken[0] == lexer.END_OF_INPUT:
        parseError("Expected Identifier but got END OF FILE")
    if not nextToken[0] == lexer.STRING_TOKEN:
        parseError("Expected String "+" but got "+ nextToken[1])
    else: 
        return nextToken

def parseProg():
    parseStmt_list()

def parseStmt_list():
    if peek("print") or peek("get") or peekID() or peek("if") or peek("while"):
        parseStmt()
        expect(";")
        parseStmt_list()

def parseStmt():
    if peek("print"):
        parsePrint()
    elif peek("get"):
        parseInput()
    elif peekID():
        parseAssign()
    elif peek("if"):
        parseIf()
    elif peek("while"):
        parseWhile()
    else:
        parseError("in parseStmt: invalid command")

def parsePrint():
    expect("print")
    val = parseParg()
    mainScope.addCommand(["print", val])

def parseParg():
    if peekSTR():
        str_ = expectSTR()
        return str_
    else:
        value = parseExpr()
        return value

def parseInput():
    expect("get")
    id_ = expectID()
    mainScope.addCommand(["get", id_])

def parseAssign():
    id_ = expectID()
    expect("=")
    value = parseExpr()
    mainScope.addCommand(["assign", id_, value])

def parseIf():
    expect("if")
    condition = parseExpr()
    expect("then")
    global mainScope
    thenScope = Scope(mainScope)
    mainScope = thenScope
    parseStmt_list()
    thenCommands = mainScope.getCommandsList()
    mainScope = mainScope.getParent()
    expect("else")
    elseScope = Scope(mainScope)
    mainScope = elseScope
    parseStmt_list()
    elseCommands = mainScope.getCommandsList()
    mainScope = mainScope.getParent()
    expect("end")
    mainScope.addCommand(["if",condition, thenCommands, elseCommands])

def parseWhile():
    expect("while")
    condition = parseExpr()
    expect("do")
    global mainScope
    doScope = Scope(mainScope)
    mainScope = doScope
    parseStmt_list()
    doCommands = mainScope.getCommandsList()
    mainScope = mainScope.getParent()
    expect("end")
    mainScope.addCommand(["while",condition, doCommands])

def parseExpr():
    a = parseN_expr()
    b = parseB_expr()
    if a is None:
        return b
    elif b is None:
        return a
    return [a, b]

def parseB_expr():
    if peek("and"):
        expect("and")
        op = "and"
        n = parseN_expr()
        return [op, n]
    elif peek("or"):
        op = "or"
        expect("or")
        n = parseN_expr()
        return [op, n]

def parseN_expr():
    a = parseTerm()
    b = parseT_expr()
    if a is None:
        return b
    elif b is None:
        return a
    return [a, b]

def parseT_expr():
    if peek("+"):
        op = "+"
        expect("+")
        n = parseN_expr()
        return [op, n]
    elif peek("-"):
        op = "-"
        expect("-")
        n = parseN_expr()
        return [op, n]

def parseTerm():
    a = parseFactor()
    b = parseF_expr()
    if a is None:
        return b
    elif b is None:
        return a
    return [a, b]

def parseF_expr():
    if peek("*"):
        op = "*"
        expect("*")
        t = parseTerm()
        return [op, t]
    elif peek("/"):
        op = "/"
        expect("/")
        t = parseTerm()
        return [op, t]
    elif peek("%"):
        op = "%"
        expect("%")
        t = parseTerm()
        return [op, t]

def parseFactor():
    a = parseValue()
    b = parseV_expr()
    if a is None:
        return b
    elif b is None:
        return a
    return [a, b]

def parseV_expr():
    if peek(">"):
        op = ">"
        expect(">")
        val_ = parseValue()
        # print([op, val_])
        return [op, val_]
    elif peek(">="):
        op = ">="
        expect(">=")
        val_ = parseValue()
        return [op, val_]
    elif peek("<"):
        op = "<"
        expect("<")
        val_ = parseValue()
        return [op, val_]
    elif peek("<="):
        op = "<="
        expect("<=")
        val_ = parseValue()
        return [op, val_]
    elif peek("=="):
        op = "=="
        expect("==")
        val_ = parseValue()
        return [op, val_]
    elif peek("!="):
        op = "!="
        expect("!=")
        val_ = parseValue()
        return [op, val_]

def parseValue():
    # print("here in value")
    if peekID():
        id_ = expectID()
        # print("id: ", id_)
        return id_
    elif peekNUM():
        num_ = expectNUM()
        # print("num: ", num_)
        return num_
    elif peek("("):
        # print("here for (")
        expect("(")
        exp = parseExpr()
        # print(exp)
        expect(")")
        return exp
    elif peek("not"):
        op = "not"
        expect("not")
        val_ = parseValue()
        return [op, val_]
    elif peek("-"):
        op = "-"
        expect("-")
        val_ = parseValue()
        return [op, val_]
    else:
        parseError("in parseValue: invalid value")

def parse(file):
    global input
    
    with open(file) as f:
      input = list(f.read())

    parseProg()
    return mainScope.getCommandsList()