#interprets a language, given a rightmost derivation.
#currently works for the example language given on http://en.wikipedia.org/wiki/LR_parser:
#    (1) E -> E * B
#    (2) E -> E + B
#    (3) E -> B
#    (4) B -> 0
#    (5) B -> 1 

class Stack:
    def __init__(self):
        self.data = []
    def push(self, value):
        self.data.append(value)
    def pop(self):
        return self.data.pop()
    def top(self):
        return self.data[-1]

class Expr:
    def __init__(self):
        self.operator = None
        self.left = None
        self.right = None
    def eval(self):
        if self.operator == "bin":
            return self.left.eval()
        if self.operator == "*":
            return self.left.eval() * self.right.eval()
        if self.operator == "+":
            return self.left.eval() + self.right.eval()
        raise Exception("couldn't recognize operator")

class Bin:
    def __init__(self):
        self.val = None
    def eval(self):
        if self.val == 0:
            return 0
        if self.val == 1:
            return 1
        raise Exception("couldn't eval Bin")

def parseExpr(symbols):
    ret = Expr()
    x = symbols.pop()
    if x == 1:
        ret.operator = "*"
        ret.right = parseBin(symbols)
        ret.left = parseExpr(symbols)
        return ret
    if x == 2:
        ret.operator = "+"
        ret.right = parseBin(symbols)
        ret.left = parseExpr(symbols)
        return ret
    if x == 3:
        ret.operator = "bin"
        ret.left = parseBin(symbols)
        return ret
    raise Exception("unexpected rule {}".format(x))

def parseBin(symbols):
    ret = Bin()
    x = symbols.pop()
    if x == 4:
        ret.val = 0
        return ret
    if x == 5:
        ret.val = 1
        return ret
    raise Exception("unexpected rule {}".format(x))

def interpret(rightDerivation):
    symbols = Stack()
    symbols.data = rightDerivation
    tree = parseExpr(symbols)
    return tree.eval()

def example():
    #the rules list 2,5,1,5,2,4,3,5
    #translates to:
    #E            (2,5,1,5,2,4,3,5)
    #(E+B)          (5,1,5,2,4,3,5)
    #(E+1)            (1,5,2,4,3,5)
    #((E*B)+1)          (5,2,4,3,5)
    #((E*1)+1)            (2,4,3,5)
    #(((E+B)*1)+1)          (4,3,5)
    #(((E+0)*1)+1)            (3,5)
    #(((B+0)*1)+1)              (5)
    #(((1+0)*1)+1)               ()
    #expected result: 2
    #(Hint: in a rightmost derivation, the nonterminal symbol farthest to the right is the one replaced.)

    rules = list(reversed([2,5,1,5,2,4,3,5]))
    print interpret(rules)