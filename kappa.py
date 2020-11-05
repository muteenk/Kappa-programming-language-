#####################
# Imports
#####################

import re
import argparse as ar

#####################
# Constants
#####################

NUMBERS = "1234567890"

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

C_STRING = "^[\"][\"]$"

#####################
# Tokens
#####################

T_STRING = "STR"
T_INT = "INT"
T_FLOAT = "FLOAT"
T_PLUS = "PLUS"
T_MIN = "MINUS"
T_MUL = "MULTIPLY"
T_DIV = "DIVIDE"
T_NOT = "NOT"
T_ASIGN = "ASSIGN"
T_EQUAL = "EQUAL"
T_NOTEQUAL = "NOTEQUAL"
T_LESS = "LESS"
T_GREATER = "GREATER"
T_LEQUAL = "LEQUAL"
T_GEQUAL = "GEQUAL"
T_LCURL = "LCURLY"
T_RCURL = "RCURLY"
T_LBRAC = "LBRACKET"
T_RBRAC = "RBRACKET"
T_LPAREN = "LPARENTHESIS"
T_RPAREN = "RPARENTHESIS"
T_NEWLINE = "NLINE"


#####################
# Errors
#####################

def error(errType, line):
    return "kappaError:\n\t" + errType + "\n\toccured at line" + str(line)


#####################
# Lexer
#####################

class Lexer:
    def __init__(self, text):
        self.line = 1
        self.text = text
        self.pos = -1
        self.currentChar = None
        self.shiftChar()


    # TO SHIFT THE CURRENT CHARACTER
    def shiftChar(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.currentChar = self.text[self.pos]
        else:
            self.currentChar = None


    # TO BUILD TOKENS BASED ON EACH CHARACTER
    def makeTokens(self):
        tokens = []

        while self.currentChar != None:
            if self.currentChar == " " or self.currentChar == "\t" or self.currentChar == "\n" or self.currentChar == "":
                if self.currentChar == "\n":
                    tokens.append(self.tokenizer(T_NEWLINE, r"\n"))
                    self.line += 1
                self.shiftChar()
            elif self.currentChar in NUMBERS or self.currentChar == ".":
                tokens.append(self.numToken())
                self.shiftChar()
            elif self.currentChar == "+":
                tokens.append(self.tokenizer(T_PLUS, '+'))
                self.shiftChar()
            elif self.currentChar == "-":
                tokens.append(self.tokenizer(T_MIN, '-'))
                self.shiftChar()
            elif self.currentChar == "*":
                tokens.append(self.tokenizer(T_MUL, '*'))
                self.shiftChar()
            elif self.currentChar == "/":
                tokens.append(self.tokenizer(T_DIV, '/'))
                self.shiftChar()
            elif self.currentChar == "!":
                tokens.append(self.tokenizer(T_NOT, '!'))
                self.shiftChar()
            elif self.currentChar == "(":
                tokens.append(self.tokenizer(T_LPAREN, '('))
                self.shiftChar()
            elif self.currentChar == ")":
                tokens.append(self.tokenizer(T_RPAREN, ')'))
                self.shiftChar()
            elif self.currentChar == "{":
                tokens.append(self.tokenizer(T_LCURL, '{'))
                self.shiftChar()
            elif self.currentChar == "}":
                tokens.append(self.tokenizer(T_RCURL, '}'))
                self.shiftChar()
            elif self.currentChar == "[":
                tokens.append(self.tokenizer(T_LBRAC, '['))
                self.shiftChar()
            elif self.currentChar == "]":
                tokens.append(self.tokenizer(T_RBRAC, ']'))
                self.shiftChar()
            elif self.currentChar == "<":
                tokens.append(self.tokenizer(T_LESS, '<'))
                self.shiftChar()
            elif self.currentChar == ">":
                tokens.append(self.tokenizer(T_GREATER, '>'))
                self.shiftChar()
            elif self.currentChar == "=":
                tokens.append(self.tokenizer(T_ASIGN, '='))
                self.shiftChar()
            elif self.currentChar in "\"" or self.currentChar in "\'":
                temp_bool = self.strToken()

                if type(temp_bool) == dict:
                    tokens.append(temp_bool)
                    self.shiftChar()
                elif type(temp_bool) == str:
                    return temp_bool
            else:
                # show some error
                e = "invalid character error ('" + self.currentChar + "')"
                return error(e, self.line)

        return tokens


    # HELPING TO CREATE TOKENS
    def tokenizer(self, _type, val):
        self.type = _type
        self.value = val

        return {self.type: self.value}


    # CREATING NUMBER TOKENS
    def numToken(self):
        dots = 0
        num_str = ""
        while True:
            if self.currentChar in NUMBERS:
                num_str = num_str + str(self.currentChar)
                if self.pos + 1 < len(self.text):
                    if self.text[self.pos + 1] in NUMBERS or self.text[self.pos + 1] == ".":
                        self.shiftChar()
                    else:
                        break
                else:
                    break
            elif self.currentChar == ".":
                num_str = num_str + self.currentChar
                dots += 1
                if dots > 1:
                    break
                self.shiftChar()
            else:
                break

        if "." in num_str:
            temp_token = self.tokenizer(T_FLOAT, num_str)

        else:
            temp_token = self.tokenizer(T_INT, num_str)

        return temp_token


    # CREATING STRING TOKEN
    def strToken(self):
        emp_str = ""
        strType = self.currentChar
        self.shiftChar()
        while True:
            if strType == "\"":
                if self.currentChar == "\"":
                    break
                else:
                    emp_str += self.currentChar
                    if self.pos + 1 < len(self.text):
                        self.shiftChar()
                    else:
                        return error("missing (\") at the end of a string", self.line)

            elif strType == "\'":
                if self.currentChar == "\'":
                    break
                else:
                    emp_str += self.currentChar
                    if self.pos + 1 < len(self.text):
                        self.shiftChar()
                    else:
                        return error("missing (\') at the end of a string", self.line)

        return self.tokenizer(T_STRING, emp_str)


#####################
# Parser
####################

class Parser:
    def __init__(self, tok):

        self.tok = tok
        self.currentTok = None
        self.tok_pos = -1
        self.line = 1
        self.shiftTok()

    def shiftTok(self):
        self.tok_pos += 1
        if self.tok_pos < len(self.tok):
            self.currentTok = self.tok[self.tok_pos]
        else:
            self.currentTok = None


    def parseCalc(self):
        calc = ""
        for tkn in self.tok:
            for key, value in tkn.items():
                self.shiftTok()
                calc += value

        return eval(calc)


    def parseStr(self):
        newStr = ""
        for tkn in self.tok:
            for key, value in tkn.items():
                self.shiftTok()
                newStr += value

        return newStr

    def oppStr(self):
        newStr = ''

        for tkn in self.tok:
            for key, value in tkn.items():
                self.shiftTok()
                if key == T_STRING:
                    toadd = '"'+value+'"'
                    newStr += toadd
                elif key == T_PLUS or key == T_MUL or key == T_INT or key == T_FLOAT :
                    newStr += value
                else:
                    return 'error'

        return eval(newStr)


    def main(self):

        str_count = 0
        str_opp_count = 0

        for tkn in self.tok:
            for key, value in tkn.items():
                if key == T_STRING:
                    str_count += 1
                elif key == T_PLUS or key == T_MUL:
                    str_opp_count += 1

        if str_count == 0 and (str_opp_count != 0 or str_opp_count == 0):
            return self.parseCalc()
        elif str_count != 0 and str_opp_count == 0:
            return self.parseStr()
        elif str_count != 0 and str_opp_count != 0:
            return self.oppStr()


#####################
# Main Function
#####################


def exec(text):
    lexer = Lexer(text)
    token = lexer.makeTokens()
    parser = Parser(token)
    try:
        return parser.main()

    except:
        return token