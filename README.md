# Compiler-form-Scratch-

list of files:
1. lexer.py (contains the lexer code)
2. myparser.py (contains the parser code)
3. myinterpreter.py (contains the interpreter code)
4. code.txt (sample code to run)

How to run:
place all the 4 files in the same folder
enter in commandprompt => python -u myinterpreter.py code.txt 

Notes:
1. Lexer code is updated, I added the functionality of strings and some other small lexemes
2. Parser code is updated, I have updated the functions in such a way that it makes commands for the interpreter to run them.    Parser sends a list of commands for the interpreter to run
3. There is an addition of Scope class that basically separates the commands of different scope i.e. if, while and main scope
4. Interpreter code is added that has an interpret function that runs the commands. It has a for loop for the list and one by    one checks which command it is and runs it accordingly
5. I have added an expression computer class that basically computes the expression by using a stack!
