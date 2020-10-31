#####################
# Constants
#####################

NUMBERS = "1234567890"

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

#####################
# Errors
#####################


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
T_ASIGN = "ASSIGN"
T_EQUAL = "EQUAL"
T_LESS = "LESS"
T_GREATER = "GREATER"
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

    def shiftChar(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.currentChar = self.text[self.pos]
        else:
            self.currentChar = None

    def makeTokens(self):
        tokens = []

        while self.currentChar != None:
            if self.currentChar == " " or self.currentChar == "\t" or self.currentChar == "\n" or self.currentChar == "":
                self.shiftChar()
            elif self.currentChar in NUMBERS:
                tokens.append(self.numToken(self.currentChar))
            elif self.currentChar == "+":
                tokens.append(self.tokenizer(T_PLUS))
                self.shiftChar()
            elif self.currentChar == "-":
                tokens.append(self.tokenizer(T_MIN))
                self.shiftChar() 
            elif self.currentChar == "*":
                tokens.append(self.tokenizer(T_MUL))
                self.shiftChar()   
            elif self.currentChar == "/":
                tokens.append(self.tokenizer(T_DIV))
                self.shiftChar()
            elif self.currentChar == "(":
                tokens.append(self.tokenizer(T_LPAREN))
                self.shiftChar()
            elif self.currentChar == ")":
                tokens.append(self.tokenizer(T_RPAREN))
                self.shiftChar()
            elif self.currentChar == "{":
                tokens.append(self.tokenizer(T_LCURL))
                self.shiftChar()
            elif self.currentChar == "}":
                tokens.append(self.tokenizer(T_RPAREN))
                self.shiftChar()
            elif self.currentChar == "[":
                tokens.append(self.tokenizer(T_LBRAC))
                self.shiftChar()
            elif self.currentChar == "]":
                tokens.append(self.tokenizer(T_RBRAC))
                self.shiftChar()
            elif self.currentChar == "<":
                tokens.append(self.tokenizer(T_LESS))
                self.shiftChar()
            elif self.currentChar == ">":
                tokens.append(self.tokenizer(T_GREATER))
                self.shiftChar()
            elif self.currentChar == "=":
                tokens.append(self.tokenizer(T_ASIGN))
                self.shiftChar()
            elif self.currentChar == "==":
                tokens.append(self.tokenizer(T_EQUAL))
                self.shiftChar()
            else:
                #show some error
                pass


        return tokens

    def tokenizer(self, _type, val=None):
        self.type = _type
        self.value = val
        if self.value != None:
            return f"{self.value}:{self.type}"
        else:
            return f"{self.type}"

    def numToken(self, num):
        self.number = num
        pass


#####################
# Main Function
#####################


def exec(text):
    lexer = Lexer(text)
    token = lexer.makeTokens()
    
    return token
