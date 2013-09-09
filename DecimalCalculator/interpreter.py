#interprets a language, given a rightmost derivation.

class Stack:
    def __init__(self):
        self.data = []
    def push(self, value):
        self.data.append(value)
    def pop(self):
        return self.data.pop()
    def top(self):
        return self.data[-1]

class NumberExpression:
    def __init__(self, number):
        self.number = number
    def eval(self):
        return self.number.eval()

class BinExpression:
    def __init__(self, left, right, binaryOperator):
        self.left = left
        self.right = right
        self.binaryOperator = binaryOperator
    def eval(self):
        return self.binaryOperator.eval(self.left.eval(), self.right.eval())

class ParenExpression:
    def __init__(self, expression):
        self.expression = expression
    def eval(self):
        return self.expression.eval()

class BinaryOperator:
    def __init__(self, symbol):
        self.symbol = symbol
    def eval(self, left, right):
        if self.symbol == "+": return left + right
        if self.symbol == "-": return left - right
        if self.symbol == "*": return left * right
        if self.symbol == "/": return left / right

class SingleDigitNumber:
    def __init__(self, digit):
        self.digit = digit
    def eval(self):
        return self.digit.eval()

class MultiDigitNumber:
    def __init__(self, remainder, lastDigit):
        self.remainder = remainder
        self.lastDigit = lastDigit
    def eval(self):
        return 10* self.remainder.eval() + self.lastDigit.eval()

class Digit:
    def __init__(self, symbol):
        self.symbol = symbol
    def eval(self):
        return int(self.symbol)

def parseExpression(symbols):
    x = symbols.pop()
    if x == 1:
        num = parseNumber(symbols)
        return NumberExpression(num)
    if x == 2:
        right = parseExpression(symbols)
        op = parseBinaryOperator(symbols)
        left = parseExpression(symbols)
        return BinExpression(left, right, op)
    if x == 3:
        return ParenExpression(parseExpression(symbols))
    raise Exception("unexpected symbol")

def parseBinaryOperator(symbols):
    x = symbols.pop()
    if x == 4: return BinaryOperator("+")
    if x == 5: return BinaryOperator("-")
    if x == 6: return BinaryOperator("*")
    if x == 7: return BinaryOperator("/")
    raise Exception("unexpected symbol")

def parseNumber(symbols):
    x = symbols.pop()
    if x == 8:
        digit = parseDigit(symbols)
        return SingleDigitNumber(digit)
    if x == 9:
        lastDigit = parseDigit(symbols)
        remainder = parseNumber(symbols)
        return MultiDigitNumber(remainder, lastDigit)
    raise Exception("unexpected symbol")

def parseDigit(symbols):
    x = symbols.pop()
    if x == 10: return Digit("0")
    if x == 11: return Digit("1")
    if x == 12: return Digit("2")
    if x == 13: return Digit("3")
    if x == 14: return Digit("4")
    if x == 15: return Digit("5")
    if x == 16: return Digit("6")
    if x == 17: return Digit("7")
    if x == 18: return Digit("8")
    if x == 19: return Digit("9")
    raise Exception("unexpected symbol")

def interpret(rightDerivation):
    symbols = Stack()
    symbols.data = rightDerivation
    tree = parseExpression(symbols)
    return tree.eval()