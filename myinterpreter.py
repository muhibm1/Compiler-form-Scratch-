import myparser
import lexer
import sys

class ExpressionComputor:
    def __init__(self, expr):
        self.expr = expr
        self.stack = []

    def evaluate(self, value):
        if value[0] == lexer.INT_TOKEN:
            return int(value[1])
        elif value[0] == lexer.ID_TOKEN:
            if value[1] not in myparser.symtab:
                print("Interpreter Error: Undefined variable '" , value[1] , "'")
                exit()
            return myparser.symtab[value[1]]

    def operate(self, op):
        if op == "not":
            a = self.stack.pop()
            self.stack.append(not a)
        elif op == '-' and len(self.stack) < 2:
            a = self.stack.pop()
            self.stack.append(-a)
        else:
            # a op b
            b = self.stack.pop()
            a = self.stack.pop()
            if op == "and":
                self.stack.append(a and b)
            elif op == "or":
                self.stack.append(a or b)
            elif op == "+":
                self.stack.append(a + b)
            elif op == "-":
                self.stack.append(a - b)
            elif op == "*":
                self.stack.append(a * b)
            elif op == "/":
                self.stack.append(a / b)
            elif op == "%":
                self.stack.append(a % b)
            elif op == ">":
                self.stack.append(a > b)
            elif op == ">=":
                self.stack.append(a >= b)
            elif op == "<":
                self.stack.append(a < b)
            elif op == "<=":
                self.stack.append(a <= b)
            elif op == "==":
                self.stack.append(a == b)
            elif op == "!=":
                self.stack.append(a != b)

    def simplify(self, lst):
        if isinstance(lst, list):
            if isinstance(lst[0], int): # ID or number
                self.stack.append(self.evaluate(lst))
            elif isinstance(lst[0], str): # operator
                op = lst[0]
                self.simplify(lst[1])
                self.operate(op)
            else:
                for l in lst:
                    self.simplify(l)


    def compute(self):
        self.simplify(self.expr)
        if len(self.stack) >= 1:
            return self.stack[0]
        return False

def computeExpression(expr):
    e = ExpressionComputor(expr)
    return e.compute()

def evaluate(value):
    if value[0] == lexer.INT_TOKEN:
        return int(value[1])
    elif value[0] == lexer.ID_TOKEN:
        if value[1] not in myparser.symtab:
            print("Interpreter Error: Undefined variable '" , value[1] , "'")
            exit()
        return myparser.symtab[value[1]]
    elif value[0] == lexer.STRING_TOKEN:
        return evaluateString(value[1])

def evaluateString(str):
    return str.replace("\\t","\t").replace("\\n","\n")

def interpret(commands):
    for c in commands:
        if c[0] == "print":
            print(evaluate(c[1]), end =" ")
        elif c[0] == "get":
            myparser.symtab[c[1][1]] = int(input(""))
        elif c[0] == "assign":
            myparser.symtab[c[1][1]] = int(computeExpression(c[2]))
        elif c[0] == "if":
            cond = bool(computeExpression(c[1]))
            if cond:
                interpret(c[2])
            else:
                interpret(c[3])
        elif c[0] == "while":
            cond = bool(computeExpression(c[1]))
            while cond:
                interpret(c[2])
                cond = bool(computeExpression(c[1]))
        else:
            print("invalid command :" + c[0])
            exit()


if len(sys.argv) < 1:
    print("Please give a program file")
else:
    commands = myparser.parse(sys.argv[1])
    interpret(commands)
    # for c in commands:
    #     print(c)
    # print("PARSED!!!!")
    # l = [[[[0, 'x'], ['>', [[0, 'y'], ['+', [1, 1]]]]], ['and', [0, 'y']]], ['-', [0, 'z']]]
    # e = ExpressionComputor(l)
    
    # print(e.compute())
