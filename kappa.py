#####################
# Imports
#####################

import re
import argparse as ar

#####################
# Constants
#####################

NUMBERS = "1234567890"

CHARS = "_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

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
T_VAR = "VAR"

#####################
# BUILT OBJECTS 
#####################

PRE_OBJECTS = [T_VAR, T_STRING, T_INT, T_FLOAT]

######################
# VARIABLE LIST
######################

varList = []


#####################
# Errors
#####################

def error(errType, line, pos=None):
    if pos:
        return "kappaError:\n\t" + errType + ";\n\toccured in <line" + str(line) + '> at <character' + str(pos + 1) + '>'
    else:
        return "kappaError:\n\t" + errType + ";\n\toccured in <line" + str(line) + '>'



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

            elif self.currentChar in CHARS:
                temp_type = self.varToken()
                if type(temp_type) == dict:
                    tokens.append(temp_type)
                    continue
                elif type(temp_type) == str:
                    return temp_type

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
                tokens.append(self.tokenizer(T_NOT, "!"))
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
                recent_tok = tokens[len(tokens)-1]

                for i in recent_tok:
                    recent_tok_type = i

                if recent_tok_type == T_VAR:
                    tokens.append(self.tokenizer(T_ASIGN, '='))
                else:
                    e = "invalid operator error (=)"
                    return error(e, self.line, self.pos)
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
                return error(e, self.line, self.pos)

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
                elif self.currentChar == None:
                    return error("missing (\") at the end of a string", self.line, self.pos - 1)
                else:
                    emp_str += self.currentChar
                    if self.pos + 1 < len(self.text):
                        self.shiftChar()
                    else:
                        return error("missing (\") at the end of a string", self.line , self.pos)

            elif strType == "\'":
                if self.currentChar == "\'":
                    break
                elif self.currentChar == None:
                    return error("missing (\') at the end of a string", self.line, self.pos - 1)
                else:
                    emp_str += self.currentChar
                    if self.pos + 1 < len(self.text):
                        self.shiftChar()
                    else:
                        return error("missing (\') at the end of a string", self.line, self.pos)

        return self.tokenizer(T_STRING, emp_str)


    def varToken(self):
        var_str = "" 

        while self.currentChar != None: 
            if self.currentChar not in CHARS and self.currentChar not in NUMBERS: 
                break
            else:
                var_str += self.currentChar
                self.shiftChar()

        
        return self.tokenizer(T_VAR, var_str)

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

    def main(self):

        str_count = 0
        str_opp_count = 0
        var_count = 0

        for tkn in self.tok:
            for key, value in tkn.items():
                if key == T_STRING:
                    str_count += 1
                elif key == T_VAR:
                    var_count += 1
                elif key == T_PLUS or key == T_MUL or key == T_DIV or key == T_MUL:
                    str_opp_count += 1
                elif key == T_EQUAL or key == T_NOTEQUAL or key == T_LEQUAL or key == T_GEQUAL:
                    str_opp_count += 1
                elif key == T_GREATER or key == T_LESS or key == T_LPAREN or key == T_RPAREN:
                    str_opp_count += 1
                elif key == T_ASIGN or key == T_LBRAC or key == T_RBRAC or key == T_RCURL or key == T_LCURL:
                    str_opp_count += 1


        if str_count == 0 and var_count == 0:
            return self.parseCalc()
        elif str_count != 0 and str_opp_count == 0 and var_count == 0:
            return self.parseStr()
        elif str_count != 0 and str_opp_count != 0 and var_count == 0:
            return self.oppStr()
        elif var_count > 0:
            return self.parseVar()

    def parseVar(self):
        varnm = self.tok[0][T_VAR]
        self.shiftTok()
        
        for x in self.currentTok:
            if self.currentTok[x] == "=":
                self.shiftTok()
                for y in self.currentTok:
                    if y in PRE_OBJECTS:
                        for z in varList:
                            if varnm == z[0]:
                                z[1] = self.currentTok[y]
                                return None
                            else:
                                lst = [varnm, self.currentTok[y], y]
                                varList.append(lst)
                                return None
                    else:
                        return error("invalid value assigned to variable (" + varnm + ")", self.line)
            else:
                for y in varList:
                    if varnm == y[0]:
                        return y[1]
                    else:
                        return error("variable (" + varnm + ") is not defined", self.line)
                
                

        




    def parseCalc(self):
        calc = ""
        for tkn in self.tok:
            for key, value in tkn.items():

                calc += value
        self.shiftTok()

        return eval(calc)


    def parseStr(self):
        newStr = ""
        for tkn in self.tok:
            for key, value in tkn.items():

                newStr += value
            self.shiftTok()

        return newStr

    def oppStr(self):
        newStr = ''
        currOpp = ''
        for tkn in self.tok:

            for key, value in tkn.items():
                ln = len(newStr)
                if currOpp == '*' and key == T_STRING:
                    e = "can't multiply string value ({0}) with a string".format(value)
                    return error(e, self.line, ln)
                elif currOpp == '*' and key == T_INT:
                    newStr += value
                elif currOpp == '+' and key == T_INT:
                    e = "can't add the integer value ({0}) with a string".format(value)
                    return error(e, self.line, ln)
                elif key == T_STRING:
                    to_add = '"'+value+'"'
                    newStr += to_add
                elif key == T_PLUS or key == T_MUL:
                    newStr += value
                    currOpp = value
                elif key == T_LPAREN or key == T_RPAREN:
                    newStr += value
                elif key == T_FLOAT:
                    e = "can't perform an operation on float value ({0}) with string".format(value)
                    return error(e, self.line, ln)
                else:
                    e = 'invalid operator/(character) ({0}) for string'.format(value)
                    return error(e, self.line, ln)

            self.shiftTok()
        return eval(newStr)



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