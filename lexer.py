#!/usr/bin/python

import sys


# Print error message and exit
def fatal(errmsg):
    print(errmsg)
    print("USAGE: \t$ lexer <path to file>\n")
    exit(0)


# Open file to lex
def openFile(filename):
    data = open(filename, "r").read()
    return data


# Check for correct number of params
def checkParams(args):
    if len(args) != 2:
        return False
    else:
        return True


# Print Error message
def errorMsg(error):
    return "ERROR: " + error + "\n"


# Print Keyword message
def keywordMsg(keyword):
    return "KEYWORD: " + keyword + "\n"


# Print ID message
def idMsg(id):
    return "ID: " + id + "\n"


# Print NUM message
def numMsg(num):
    return "NUM: " + num + "\n"


# Perform lexical analysis
def lexer(data):
    keywords = ("else", "if", "int", "return", "void", "while", "float")
    operators = ("+", "-", "*", ";", ",", "(", ")",
                 "[", "]", "{", "}", "/*", "*/")

    line = ""
    output = ""

    # Iterate over each character in data, store in 'line' variable
    for char in range(0, len(data)):
        line += data[char]

        # Once '\n' is read or end of file is reached, line is loaded
        if data[char] == '\n' or char == (len(data) - 1):
            line += "\n"

            # Skip blank lines
            if not line[0] == '\n':
                # output += "\nINPUT: " + line

                # Buffers
                commentBuffer = ""
                alphaBuffer = ""
                digitBuffer = ""
                lexeme = ""
                opBuffer = ""
                errorBuffer = ""

                # States
                alphaState = False
                digitState = False
                commentState = False
                errorState = False
                opState = False
                floatState = False

                # Counts
                nestedCount = 0

                for token in line:

                    # Handle comments
                    if commentState:
                        if token == '/':
                            break
                        elif token == '*':
                            commentState = False
                            commentBuffer = ""
                            token = ""
                            lexeme = ""
                            nestedCount += 1
                        else:
                            output += commentBuffer + "\n"
                            commentState = False
                            commentBuffer = ""

                    # Handle block comments
                    if nestedCount > 0:
                        if token == '*':
                            if commentBuffer == '/':
                                nestedCount += 1
                                commentBuffer = ""
                            else:
                                commentBuffer = "*"
                        elif token == '/':
                            if commentBuffer == "":
                                commentBuffer = '/'

                            elif commentBuffer == '*':
                                commentBuffer = ""
                                nestedCount -= 1
                                token = " "
                        elif token == '\n':
                            commentBuffer = ""
                            nestedCount = 0
                        else:
                            commentBuffer = ""

                    # Handle non-comments
                    else:

                        # Handle errors
                        if errorState:
                            if (not token == '\n' and not token == ' '):
                                errorBuffer += token
                            else:
                                output += errorMsg(errorBuffer)
                                errorState = False

                        # Handle non-errors
                        else:
                            if token == '/':
                                if(alphaState):
                                    if lexeme in keywords:
                                        output += keywordMsg(lexeme)
                                    else:
                                        output += idMsg(lexeme)
                                    alphaBuffer = ""
                                    lexeme = ""
                                    alphaState = False

                                if(digitState):
                                    output += numMsg(lexeme)
                                    digitBuffer = ""
                                    lexeme = ""
                                    digitState = False

                                commentState = True
                                commentBuffer = token

                            # Keeps track of operators
                            if opState:
                                if token == '=':
                                    opBuffer += token
                                    opState = False
                                    output += opBuffer + "\n"
                                    opBuffer = ""
                                else:
                                    output += opBuffer + "\n"
                                    opState = False
                                    opBuffer = ""
                            else:
                                if (token == '<' or token == '>' or token == '!' or token == '='):
                                    opBuffer += token
                                    opState = True
                                    if digitState:
                                        output += numMsg(lexeme)
                                        digitBuffer = ""
                                        lexeme = ""
                                        digitState = False
                                    if alphaState:
                                        if lexeme in keywords:
                                            output += keywordMsg(lexeme)
                                        else:
                                            output += idMsg(lexeme)
                                        alphaBuffer = ""
                                        lexeme = ""
                                        alphaState = False

                            if token in operators:
                                if digitState:
                                    if floatState:
                                        if token == '+' or token == '-':
                                            digitBuffer += token
                                            lexeme += token
                                        if token == ';':
                                            output += numMsg(lexeme)
                                            digitBuffer = ""
                                            lexeme = ""
                                            floatState = False
                                    else:
                                        output += numMsg(lexeme)
                                        digitBuffer = ""
                                        lexeme = ""
                                        digitState = False
                                if alphaState:
                                    if lexeme in keywords:
                                        output += keywordMsg(lexeme)
                                    else:
                                        output += idMsg(lexeme)
                                    alphaBuffer = ""
                                    lexeme = ""
                                    alphaState = False
                                if not floatState:
                                    output += token + "\n"

                            # Keeps track of alphanumeric characters
                            if token.isalnum():
                                if token.isalpha():
                                    if token == 'E':
                                        if digitState:
                                            digitBuffer += token
                                            lexeme += token
                                            floatState = True
                                    else:
                                        if digitState:
                                            output += numMsg(digitBuffer)
                                            digitState = False
                                            digitBuffer = ""
                                            lexeme = ""

                                        alphaBuffer += token
                                        lexeme += token

                                        alphaState = True

                                else:
                                    if floatState:
                                        digitBuffer += token
                                        lexeme += token
                                    else:
                                        if alphaState:
                                            output += idMsg(alphaBuffer)
                                            alphaState = False
                                            alphaBuffer = ""
                                            lexeme = ""

                                        digitBuffer += token
                                        lexeme += token

                                        digitState = True

                            if (token == '.'):
                                if digitState:
                                    lexeme += token
                                    digitBuffer += token
                                    floatState = True

                            if token == " " or token == '\n':
                                if lexeme.isalnum():
                                    if lexeme in keywords:
                                        output += keywordMsg(lexeme)
                                        lexeme = ""
                                        alphaState = False
                                        digitState = False
                                        alphaBuffer = digitBuffer = ""
                                    elif floatState:
                                        output += numMsg(lexeme)
                                        lexeme = ""
                                        alphaState = False
                                        digitState = False
                                        floatState = False
                                        alphaBuffer = digitBuffer = ""
                                    else:
                                        if lexeme.isalpha():
                                            output += idMsg(lexeme)
                                            lexeme = ""
                                            alphaState = False
                                            digitState = False
                                            alphaBuffer = digitBuffer = ""
                                        else:
                                            output += numMsg(lexeme)
                                            lexeme = ""
                                            alphaState = False
                                            digitState = False
                                            alphaBuffer = digitBuffer = ""
                                elif floatState:
                                    output += numMsg(lexeme)
                                    lexeme = ""
                                    alphaState = False
                                    digitState = False
                                    floatState = False
                                    alphaBuffer = digitBuffer = ""

                            special = ['<', '>', '!', '=', '/', ' ', '\n']
                            special.extend(operators)
                            if not token in special and not token.isalnum() and not floatState:
                                if digitState:
                                    output += numMsg(lexeme)
                                    digitBuffer = ""
                                    lexeme = ""
                                    digitState = False
                                if alphaState:
                                    if lexeme in keywords:
                                        output += keywordMsg(lexeme)
                                    else:
                                        output += idMsg(lexeme)
                                    alphaBuffer = ""
                                    lexeme = ""
                                    alphaState = False
                                errorState = True
                                errorBuffer += token

                            # Set doPrint to True for debugging
                            doPrint = False
                            if doPrint:
                                print("token:\t\t" + token)
                                print("lexeme:\t\t" + lexeme)
                                print("alphaState:\t" + str(alphaState))
                                print("digitState:\t" + str(digitState))
                                print("opState:\t" + str(opState))
                                print("floatState:\t" + str(floatState))
                                print("errorState:\t" + str(errorState))
                                print("alpha:\t\t" + alphaBuffer)
                                print("digit:\t\t" + digitBuffer)
                                print("opBuffer:\t" + opBuffer)
                                print("errorBuffer:\t" + errorBuffer)
                                print("\n")
                                print(output)

            line = ""
    return output


# Run program
def main(params):
    if not checkParams(params):
        fatal("ERROR:\tINCORRECT NUMBER OF ARGUMENTS\n")
    try:
        data = openFile(params[1])
        lexer(data)
    except OSError as e:
        print("File not found!")
        exit()
    data = openFile(params[1])


# Check how file is accessed
if __name__ == '__main__':
    main(sys.argv)
