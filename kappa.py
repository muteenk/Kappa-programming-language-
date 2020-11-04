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
# Errors
#####################


class Error:

    def __init__(self, errType, line):
        self.err = errType
        self.line


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


#####################
# Lexer
#####################

class Lexer:


    def __init__(self, text):
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
                #show some error
                a = "Not Found"
                return a

        return tokens






    # HELPING TO CREATE TOKENS
    def tokenizer(self, _type, val):
        self.type = _type
        self.value = val
        
        return {self.type:self.value}
        


    def numToken(self):
        dots = 0
        num_str = ""
        while True:
            if self.currentChar in NUMBERS:
                num_str = num_str + str(self.currentChar)
                if self.pos + 1 < len(self.text):
                    if self.text[self.pos+1] in NUMBERS or self.text[self.pos+1] == ".":
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
                        return "Missing (\") at the end of string !!!"
            
            elif strType == "\'":
                if self.currentChar == "\'":
                    break
                else:
                    emp_str += self.currentChar
                    if self.pos + 1 < len(self.text):
                        self.shiftChar()
                    else:
                        return "Missing (\') at the end of string !!!"


        return self.tokenizer(T_STRING, emp_str)






#####################
# Parser
####################

class Parser:

    def __init__(self, tok):
        self.tok = tok

    def parseCalc(self):
        calc = ""
        for tkn in self.tok:
            for key, value in tkn.items():
                calc += value

        return eval(calc)
                

    def parseStr(self):

        newStr = ""
        for tkn in self.tok:
            for key, value in tkn.items():
                newStr += value

        return newStr        





#####################
# Main Function
#####################


def exec(text):
    lexer = Lexer(text)
    token = lexer.makeTokens()
    parser = Parser(token)
    
    str_count = 0

    # return token

    try:
        for tkn in token:
            for key, value in tkn.items():
                if key == T_STRING:
                    str_count += 1
                    break
            
        if str_count == 0:
            return parser.parseCalc()
        else:
            return parser.parseStr()
    except:
        return token
                
    
