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
T_PLUS = "+"
T_MIN = "-"
T_MUL = "*"
T_DIV = "/"
T_ASIGN = "="
T_EQUAL = "=="
T_LESS = "<"
T_GREATER = ">"
T_LCURL = "{"
T_RCURL = "]"
T_LBRAC = "["
T_RBRAC = "]"
T_LPAREN = "("
T_RPAREN = ")"



class Token:

    def __init__(self, _type, val):
        self.type = _type
        self.value = val

    def __repr__(self):
        if self.value:
            return f"{self.value}:{self.type}"
        else:
            return f"{self.type}"

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
                tokens.append(self.numToken())
            elif self.currentChar == "+":
                tokens.append(Token(T_PLUS))
                self.shiftChar()
            elif self.currentChar == "-":
                tokens.append(Token(T_MIN))
                self.shiftChar() 
            elif self.currentChar == "*":
                tokens.append(Token(T_MUL))
                self.shiftChar()   
            elif self.currentChar == "/":
                tokens.append(Token(T_DIV))
                self.shiftChar()
            elif self.currentChar == "(":
                tokens.append(Token(T_LPAREN))
                self.shiftChar()
            elif self.currentChar == ")":
                tokens.append(Token(T_RPAREN))
                self.shiftChar()
            elif self.currentChar == "{":
                tokens.append(Token(T_LCURL))
                self.shiftChar()
            elif self.currentChar == "}":
                tokens.append(Token(T_RPAREN))
                self.shiftChar()
            elif self.currentChar == "[":
                tokens.append(Token(T_LBRAC))
                self.shiftChar()
            elif self.currentChar == "]":
                tokens.append(Token(T_RBRAC))
                self.shiftChar()

        return tokens


#####################
# Main Function
#####################


#####################
# Executer
#####################

def exec():
    pass

if __name__ == "__main__":
    exec()