#!/usr/bin/python3.3

from lexer import *
import sys
import inspect

#########################################
# Set to True for debug info in console #
debugSwitch = False
#########################################

terminals = ("num", "id", ";", "=", "[", "]", "int", "void", "(",
             ")", ",", "{", "}", "if", "else", "while", "return",
             "<=", "<", ">", ">=", "==", "!=", "+", "-", "*", "/", "$")
types = ("int", "float", "void")
rel = ("<=", "<", ">", ">=", "==", "!=")
multi = ("*", "/")
add = ("+", "-")
keywords = ("return", "void", "if", "int", "while", "float", "else")

index = 0               # Counter for position in symbol table
listIndex = 0           # Counter for position in list of symbol tables

table = {}              # Symbol table
tableList = [table]     # List of symbol tables for handling scope

multipleMains = False   # Check for multiple main functions
idIsVoid = False        # Check for void IDs

currentID = ""          # Keep track of current ID
currentType = ""        # Keep track of current type
funcType = ""           # Keep track of type of function


def main(args):
    '''Main routine that calls parser'''
    if not checkParams(args):
        fatal("ERROR:\tINCORRECT NUMBER OF ARGUMENTS\n")

    try:
        data = openFile(args[1])
        makeCode("1", "1", "1", "1")
        parser(lexer(data))
    except OSError as e:
        print("ERROR: File not found")
        exit(1)


def parser(data):
    global index

    tokens = data.split()
    tokens.append("$")

    if debugSwitch:
        print(tokens)
    while index < len(tokens):
        AA(tokens)
        if multipleMains == True:
            reject()


        if tokens[index] == '$':
            if debugSwitch:
                print("accept: $")
            accept(0)
    print("ERROR IN PARSE")


def makeTemp():
    ''' Generates temporary variables'''
    makeTemp.i += 1
    return "t" + str(makeTemp.i)
makeTemp.i = 0


def makeCode(operation, op1, op2, result):
    ''' Generates lines of code'''
    if makeCode.i == 0:
        print("{}\t\t{}\t\t{}\t\t{}\t\t{}".format("line", "op", "op1", "op2", 
              "result"))
    else:
        print("{}\t\t{}\t\t{}\t\t{}\t\t{}".format(makeCode.i, str(operation),
              str(op1), str(op2), str(result)))
    makeCode.i += 1
makeCode.i = 0


def accept(token):
    '''Accepts tokens'''
    global index

    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)

    if token == 0:
        print("ACCEPT")

        if debugSwitch:
            print(table)
        exit(1)

    # Set debugSwitch to True and debug info will be printed
    if debugSwitch:
        print("accept: " + token + " from " + info.function + " at " + str(
            info.lineno))

    index = index + 1


def mainTest(token):
    '''Tests if "main" has been defined'''
    if "main" in table:
        if token == "main":
            reject()


def voidTest(token):
    ''' Tests for void variable'''
    if token == "void":
        reject()


def reject():
    '''Rejects input if not parseable'''
    if debugSwitch:
        callerframerecord = inspect.stack()[1]
        frame = callerframerecord[0]
        info = inspect.getframeinfo(frame)
        # print(info.filename)                      # __FILE__     -> Test.py
        print(info.function)                     # __FUNCTION__ -> Main
        print(info.lineno)                       # __LINE__     -> 13
    print("REJECT")
    exit(1)


def debugFunc():
    '''Debug function that prints debug info if debugSwitch is True'''
    if debugSwitch:
        callerframerecord = inspect.stack()[1]
        frame = callerframerecord[0]
        info = inspect.getframeinfo(frame)
        # print(info.filename)
        print("[Called: " + info.function + "]")


def AA(tokens):
    '''First production rule in grammar'''
    global index
    global currentID
    global funcType
    varType = ""
    if tokens[index] == "ERROR:":
        reject()

    if tokens[index] == 'KEYWORD:':
        accept(tokens[index])
        if tokens[index] in types:
            funcType = tokens[index]
            varType = tokens[index]
            accept(tokens[index])
            if tokens[index] == "ID:":

                accept(tokens[index])

                # Check for duplicates
                if tokens[index] in table:
                    mainTest(tokens[index])

                table[tokens[index]] = varType
                accept(tokens[index])
                # print(table)
                AC(tokens)
                AB(tokens)
            else:
                reject()
        else:
            reject()
    else:
        reject()


def AB(tokens):
    debugFunc()
    global index
    varType = ""
    if tokens[index] in types:
        varType = tokens[index]
        accept(tokens[index])
        if tokens[index] == "ID:":
            accept(tokens[index])
            table[tokens[index]] = varType
            accept(tokens[index])
            AC(tokens)
            AB(tokens)
            return
        else:
            reject()
    if tokens[index] == "$":
        return


def AC(tokens):
    debugFunc()
    global index
    if tokens[index] == ";" or tokens[index] == "[":
        AE(tokens)
        return
    elif tokens[index] == "(":
        AG(tokens)
    else:
        reject()


def AD(tokens):
    debugFunc()
    global index
    varType = ""
    if tokens[index] in types:

        # Reject void types
        if tokens[index] == "void":
            reject()

        varType = tokens[index]
        accept(tokens[index])
        if tokens[index] == "ID:":
            accept(tokens[index])

            # Check if already declared
            if tokens[index] in table:
                reject()

            table[tokens[index]] = varType
            accept(tokens[index])
            AE(tokens)
        else:
            reject()
    else:
        reject()


def AE(tokens):
    debugFunc()
    global index
    if tokens[index] == ";":
        makeCode("alloc", "", 4, tokens[index-1])
        accept(tokens[index])
        return
    elif tokens[index] == "[":
        accept(tokens[index])
        if tokens[index] == "NUM:":
            accept(tokens[index])
            accept(tokens[index])
            makeCode("alloc", "", 4*int(tokens[index-1]), tokens[index-4])
            if tokens[index] == "]":
                accept(tokens[index])
                if tokens[index] == ";":
                    accept(tokens[index])


def AG(tokens):
    debugFunc()
    global index
    if tokens[index] == "(":
        funcName = tokens[index-1]
        makeCode("func", funcName, tokens[index+2], "0")
        accept(tokens[index])
        AH(tokens)
        if tokens[index] == ")":
            accept(tokens[index])
            AK(tokens, "func", funcName)
        else:
            reject()
    else:
        reject()


def AH(tokens):
    debugFunc()
    global index
    varType = ""
    if tokens[index] == "KEYWORD:":
        accept(tokens[index])
        if tokens[index] == "int":
            varType = "int"
            accept(tokens[index])
            if tokens[index] == "ID:":
                accept(tokens[index])
                table[tokens[index]] = varType
                accept(tokens[index])
                AJ(tokens)
                AI(tokens)
            else:
                reject()
        elif tokens[index] == "float":
            varType = "float"
            accept(tokens[index])
            if tokens[index] == "ID:":
                accept(tokens[index])
                table[tokens[index]] = varType
                accept(tokens[index])
                AJ(tokens)
                AI(tokens)
            else:
                reject()
        elif tokens[index] == "void":
            accept(tokens[index])
        else:
            reject()


def AI(tokens):
    debugFunc()
    global index
    varType = ""
    if tokens[index] == ",":
        accept(tokens[index])
        if tokens[index] == "KEYWORD:":
            accept(tokens[index])
            if tokens[index] in types:
                varType = tokens[index]
                accept(tokens[index])
                if tokens[index] == "ID:":
                    accept(tokens[index])
                    table[tokens[index]] = varType
                    accept(tokens[index])
                    AJ(tokens)
                    AI(tokens)
                else:
                    reject()
            else:
                reject()
        else:
            reject()


def AJ(tokens):
    debugFunc()
    global index
    if tokens[index] == "[":
        accept(tokens[index])
        if tokens[index] == "]":
            accept(tokens[index])
        else:
            reject()


def AK(tokens, type, name):
    debugFunc()
    global index
    if tokens[index] == "{":
        accept(tokens[index])
        AL(tokens)
        AM(tokens)
        if tokens[index] == "}":
            accept(tokens[index])
            makeCode("end", type, name, "")

        else:
            reject()
    else:
        reject()


def AL(tokens):
    debugFunc()
    global index
    if tokens[index] == "KEYWORD:" and tokens[index + 1] in types:
        accept(tokens[index])
        AD(tokens)
        AL(tokens)


def AM(tokens):
    debugFunc()
    global index
    if tokens[index] == "ID:" or tokens[index] == "NUM:" or tokens[index] == "(" or tokens[index] == "{":
        AN(tokens)
        AM(tokens)
    if tokens[index] == "KEYWORD:":
        # accept(tokens[index])
        # if tokens[index] == "if" or tokens[index] == "while" or tokens[index] == "return":
            # accept(tokens[index])
        AN(tokens)
        AM(tokens)


def AN(tokens):
    debugFunc()
    global index
    if tokens[index] == "ID:" or tokens[index] == "NUM:" or tokens[index] == "(" or tokens[index] == ";":
        AS(tokens)
    elif tokens[index] == "{":
        AK(tokens, "", "")
    elif tokens[index] == "KEYWORD:":
        accept(tokens[index])
        if tokens[index] == "if":
            AO(tokens)
        elif tokens[index] == "while":
            AQ(tokens)
        elif tokens[index] == "return":
            AR(tokens)
        else:
            reject()


def AO(tokens):
    debugFunc()
    global index
    if tokens[index] == "if":
        accept(tokens[index])
        if tokens[index] == "(":
            accept(tokens[index])
            AT(tokens)
            if tokens[index] == ")":
                accept(tokens[index])
                AN(tokens)
                AP(tokens)
            else:
                reject()
        else:
            reject()
    else:
        reject()


def AP(tokens):
    debugFunc()
    global index
    if tokens[index] == "KEYWORD:":
        accept(tokens[index])
        if tokens[index] == "else":
            accept(tokens[index])
            AN(tokens)


def AQ(tokens):
    debugFunc()
    global index
    if tokens[index] == "while":
        accept(tokens[index])
        if tokens[index] == "(":
            accept(tokens[index])
            AT(tokens)
            if tokens[index] == ")":
                accept(tokens[index])
                AN(tokens)
            else:
                reject()
        else:
            reject()
    else:
        reject()


def AR(tokens):
    debugFunc()
    global index
    if tokens[index] == "return":
        accept(tokens[index])

        # Check for void functions that return something
        if funcType == "void":
            if tokens[index] == "(" or tokens[index] == "ID:" or tokens[index] == "NUM:":
                reject()

        AS(tokens)
    else:
        reject()


def AS(tokens):
    debugFunc()
    global index
    if tokens[index] == "(" or tokens[index] == "ID:" or tokens[index] == "NUM:":
        AT(tokens)
        if tokens[index] == ";":
            accept(tokens[index])
        else:
            reject()
    elif tokens[index] == ";":
        accept(tokens[index])
    else:
        reject()


def AT(tokens):
    debugFunc()
    global index
    if tokens[index] == "ID:":
        accept(tokens[index])

        # Make sure return value matches
        if tokens[index - 2] == "return":
            if table[tokens[index]] != funcType:
                reject()

        accept(tokens[index])
        AU(tokens)
    elif tokens[index] == "(":
        accept(tokens[index])
        AT(tokens)
        if tokens[index] == ")":
            accept(tokens[index])
            BB(tokens)
            AZ(tokens)
            AX(tokens)
        else:
            reject()
    elif tokens[index] == "NUM:":
        makeCode("disp", tokens[index - 2], 4 * int(tokens[index + 1]), makeTemp())
        accept(tokens[index])
        accept(tokens[index])
        BB(tokens)
        AZ(tokens)
        AX(tokens)
    else:
        reject()


def AU(tokens):
    debugFunc()
    global index
    if tokens[index] == "[":
        AW(tokens)
        AV(tokens)
    elif tokens[index] in multi or tokens[index] in rel or tokens[index] in add or tokens[index] == "=":
        AV(tokens)
    elif tokens[index] == "(":
        makeCode("call", tokens[index - 1], "1", makeTemp())
        accept(tokens[index])
        BF(tokens)
        if tokens[index] == ")":
            accept(tokens[index])
            BB(tokens)
            AZ(tokens)
            AX(tokens)
        else:
            reject()


def AV(tokens):
    debugFunc()
    global index
    savedVar = tokens[index-1]

    if tokens[index] == "=":
        accept(tokens[index])
        AT(tokens)
        makeCode("assign", makeTemp(), "", savedVar)

    elif tokens[index] == "*" or tokens[index] == "/":
        BB(tokens)
        AZ(tokens)
        AX(tokens)

    elif tokens[index] == "+" or tokens[index] == "-":
        AZ(tokens)
        AX(tokens)

    elif tokens[index] in rel:
        AX(tokens)


def AW(tokens):
    debugFunc()
    global index
    if tokens[index] == "[":
        accept(tokens[index])
        AT(tokens)
        if tokens[index] == "]":
            accept(tokens[index])
        else:
            reject()


def AX(tokens):
    debugFunc()
    global index
    if tokens[index] in rel:
        AY(tokens)
        BD(tokens)
        BB(tokens)
        AZ(tokens)


def AY(tokens):
    debugFunc()
    global index
    if tokens[index] in rel:
        makeCode("comp", makeTemp(), tokens[index+2], makeTemp())

        if tokens[index] == ">":
            makeCode("BRG", makeTemp(), "", "")
        elif tokens[index] == "<":
            makeCode("BRL", makeTemp(), "", "")
        elif tokens[index] == ">=":
            makeCode("BRGE", makeTemp(), "", "")
        elif tokens[index] == "<=":
            makeCode("BRLE", makeTemp(), "", "")
        elif tokens[index] == "==":
            makeCode("BREQ", makeTemp(), "", "")
        elif tokens[index] == "!=":
            makeCode("BRNE", makeTemp(), "", "")

        accept(tokens[index])
    else:
        reject()


def AZ(tokens):
    debugFunc()
    global index
    if tokens[index] in add:
        BA(tokens)
        BD(tokens)
        BB(tokens)
        AZ(tokens)


def BA(tokens):
    debugFunc()
    global index
    if tokens[index] in add:
        accept(tokens[index])

        if tokens[index - 1] == "+":
            makeCode("add", makeTemp(), tokens[index + 1], makeTemp())
        else:
            makeCode("sub", makeTemp(), tokens[index + 1], makeTemp())

    else:
        reject()


def BB(tokens):
    debugFunc()
    global index
    if tokens[index] in multi:
        BC(tokens)
        BD(tokens)
        BB(tokens)


def BC(tokens):
    debugFunc()
    global index
    if tokens[index] in multi:
        accept(tokens[index])

        if tokens[index - 1] == "*":
            makeCode("mult", makeTemp(), tokens[index + 1], makeTemp())
        else:
            makeCode("div", makeTemp(), tokens[index + 1], makeTemp())



    else:
        reject()


def BD(tokens):
    debugFunc()
    global index
    if tokens[index] == "(":
        accept(tokens[index])
        AT(tokens)
        if tokens[index] == ")":
            accept(tokens[index])
        else:
            reject()
    elif tokens[index] == "ID:":
        accept(tokens[index])
        accept(tokens[index])
        BE(tokens)
    elif tokens[index] == "NUM:":
        accept(tokens[index])
        accept(tokens[index])
    else:
        reject()


def BE(tokens):
    debugFunc()
    global index
    if tokens[index] == "[":
        AW(tokens)

    elif tokens[index] == "(":
        accept(tokens[index])
        BF(tokens)
        if tokens[index] == ")":
            accept(tokens[index])
        else:
            reject()


def BF(tokens):
    debugFunc()
    global index
    if tokens[index] == "(" or tokens[index] == "ID:" or tokens[index] == "NUM:":
        BG(tokens)


def BG(tokens):
    debugFunc()
    global index
    if tokens[index] == "(" or tokens[index] == "ID:" or tokens[index] == "NUM:":
        if tokens[index] == "ID:":
            makeCode("arg", "", "", tokens[index+1])
        AT(tokens)
        BH(tokens)
    else:
        reject()


def BH(tokens):
    debugFunc()
    global index
    if tokens[index] == ",":
        accept(tokens[index])
        AT(tokens)
        BH(tokens)


# Check how file is accessed
if __name__ == '__main__':
    main(sys.argv)


class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)


class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)
