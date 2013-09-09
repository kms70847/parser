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

def getVar(scopes, name):
    for scope in scopes[::-1]:
        if name in scope:
            return scope[name]
    return None

class StatementList:
    def __init__(self, statements):
        self.statements = statements
    def eval(self, scopes):
        returnVal = None
        for statement in self.statements:
            returnVal = statement.eval(scopes)
        return returnVal

class PrintStatement:
    def __init__(self, expression):
        self.expression = expression
    def eval(self, scopes):
        print self.expression.eval(scopes)

class AssignmentStatement:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression
    def eval(self, scopes):
        scopes[-1][self.identifier.id] = self.expression.eval(scopes)

class WhileStatement:
    def __init__(self, condition, statements):
        self.condition = condition
        self.statements = statements
    def eval(self, scopes):
        while self.condition.eval(scopes):
            self.statements.eval(scopes)

class IfStatement:
    def __init__(self, condition, statements, elseStatements = None):
        self.condition = condition
        self.statements = statements
        self.elseStatements = elseStatements
    def eval(self, scopes):
        if self.condition.eval(scopes):
            self.statements.eval(scopes)
        else:
            if self.elseStatements != None:
                self.elseStatements.eval(scopes)

class ExpressionStatement:
    def __init__(self, expression):
        self.expression = expression
    def eval(self, scopes):
        return self.expression.eval(scopes)

class ValueExpression:
    def __init__(self, value):
        self.value = value
    def eval(self, scopes):
        return self.value.eval(scopes)

class BinaryOperatorExpression:
    def __init__(self, left, right, operator):
        self.left = left
        self.right = right
        self.op = operator
    def eval(self, scopes):
        return self.op.eval(scopes, self.left, self.right)

class FunctionCallExpression:
    def __init__(self, ref, arguments):
        self.ref = ref
        self.arguments = arguments
    def eval(self, scopes):
        func = self.ref.eval(scopes)
        if not isinstance(func, Function):
            raise Exception("Attempted to call nonfunction type {}".format(func.__class__.__name__))        
        return func.eval(scopes, [arg.eval(scopes) for arg in self.arguments])

class FunctionDeclarationExpression:
    def __init__(self, arguments, statements):
        self.arguments = arguments
        self.statements = statements
    def eval(self, scopes):
        return Function(scopes, self.arguments, self.statements)

#note: not part of the AST. created at eval time!
class Function:
    def __init__(self, closure, arguments, statements):
        self.closure = closure
        self.arguments = arguments
        self.statements = statements
    def eval(self, scopes, argumentValues):
        locals = {}
        for i in range(len(self.arguments)):
            name = self.arguments[i].id
            value = argumentValues[i]
            locals[name] = value
        return self.statements.eval(self.closure + [locals])

class BinaryOperator:
    def __init__(self, operator):
        self.operator = operator
    def eval(self, scopes, left, right):
        left = left.eval(scopes)
        right = right.eval(scopes)
        if self.operator == "+": 
            if isinstance(left, str):
                return left + str(right)
            elif isinstance(right, str):
                return str(left) + right
            else:
                return left  + right
        if self.operator == "-":  return left  - right
        if self.operator == "*":  return left  * right
        if self.operator == "/":  return left  / right
        if self.operator == "%":  return left  % right
        if self.operator == "==": return left == right
        if self.operator == ">":  return left  > right
        if self.operator == "<":  return left  < right

class Number:
    def __init__(self, num):
        self.num = num
        assert isinstance(num, str), "expected string, got: {}".format(self.num)
    def eval(self, scopes):
        return int(self.num)

class Identifier:
    def __init__(self, identifier):
        self.id = identifier
    def eval(self, scopes):
        var = getVar(scopes, self.id)
        if var == None:
            raise Exception("used variable {} before it was assigned".format(self.id))
        return var

class StringLiteral:
    def __init__(self, msg):
        self.msg = msg
    def eval(self, scopes):
        return self.msg

def parseStatementList(states, rules):
    state = states.pop()
    rule = rules[state]
    assert rule.LHS.value == "StatementList", "unexpected LHS {}".format(rule.LHS.value)

    if len(rule.RHS) == 1:
        statement = parseStatement(states, rules)
        return StatementList([statement])
    else:
        remainingStatements = parseStatementList(states, rules).statements
        firstStatement = parseStatement(states, rules)
        return StatementList([firstStatement] + remainingStatements)
    raise Exception("unexpected state {}".format(state))

def parseStatement(states, rules):
    state = states.pop()
    rule = rules[state]
    assert rule.LHS.value == "Statement", "unexpected LHS {}".format(rule.LHS.value)

    possibleStatements = {"Print": parsePrintStatement, "Assignment": parseAssignmentStatement, "While": parseWhileStatement, "If": parseIfStatement, "Expression": parseExpressionStatement}
    for prefix, func in possibleStatements.iteritems():
        if rule.RHS[0].value.startswith(prefix):
            return func(states, rules)
    raise Exception("unexpected state {}".format(state))

def parsePrintStatement(states, rules):
    state = states.pop()
    rule = rules[state]
    assert rule.LHS.value == "PrintStatement", "unexpected LHS {}".format(rule.LHS.value)
    return PrintStatement(parseExpression(states, rules))

def parseAssignmentStatement(states, rules):
    state = states.pop()
    rule = rules[state]
    assert rule.LHS.value == "AssignmentStatement", "unexpected LHS {}".format(rule.LHS.value)

    expr = parseExpression(states, rules)
    id = parseIdentifier(states, rules)
    return AssignmentStatement(id, expr)

def parseWhileStatement(states, rules):
    state = states.pop()
    rule = rules[state]
    assert rule.LHS.value == "WhileStatement", "unexpected LHS {}".format(rule.LHS.value)

    statements = parseStatementList(states, rules)
    condition = parseExpression(states, rules)
    return WhileStatement(condition, statements)

def parseIfStatement(states, rules):
    state = states.pop()
    rule = rules[state]
    assert rule.LHS.value == "IfStatement", "unexpected LHS {}".format(rule.LHS.value)

    elseStatements = None
    if len([token.value for token in rule.RHS if token.value == "StatementList"]) == 2:
        elseStatements = parseStatementList(states, rules)

    statements = parseStatementList(states, rules)
    condition = parseExpression(states, rules)
    return IfStatement(condition, statements, elseStatements)

def parseExpressionStatement(states, rules):
    state = states.pop()
    rule = rules[state]
    assert rule.LHS.value == "ExpressionStatement", "unexpected LHS {}".format(rule.LHS.value)
    return parseExpression(states, rules)
    
def parseExpression(states, rules):
    state = states.pop()
    rule = rules[state]
    assert rule.LHS.value == "Expression", "unexpected LHS {}".format(rule.LHS.value)

    if len(rule.RHS) == 1 and rule.RHS[0].value == "Value":
        return ValueExpression(parseValue(states, rules))
    if len(rule.RHS) == 1 and rule.RHS[0].value == "FunctionCall":
        return parseFunctionCallExpression(states, rules)
    if len(rule.RHS) == 1 and rule.RHS[0].value == "FunctionDeclaration":
        return parseFunctionDeclarationExpression(states, rules)
    if "BinaryOperator" in [token.value for token in rule.RHS]:
        right = parseValue(states, rules)
        op = parseBinaryOperator(states, rules)
        left = parseExpression(states, rules)
        return BinaryOperatorExpression(left, right, op)
    if rule.RHS[0].value == "(":
        return parseExpression(states, rules)
    raise Exception("unexpected state {}".format(state))

def parseFunctionDeclarationExpression(states, rules):
    state = states.pop()
    rule = rules[state]
    assert rule.LHS.value == "FunctionDeclaration", "unexpected LHS {}".format(rule.LHS.value)
    body = parseStatementList(states, rules)
    if "FunctionDeclarationArgumentList" in [token.value for token in rule.RHS]:
        arguments = parseFunctionDeclarationArgumentList(states, rules)
    else:
        arguments = []
    return FunctionDeclarationExpression(arguments, body)

def parseFunctionDeclarationArgumentList(states, rules):
    state = states.pop()
    rule = rules[state]
    assert rule.LHS.value == "FunctionDeclarationArgumentList", "unexpected LHS {}".format(rule.LHS.value)
    if len(rule.RHS) == 1:
        rest = []
    else:
        rest = parseFunctionDeclarationArgumentList(states, rules)
    first = [parseIdentifier(states, rules)]
    return first + rest

def parseFunctionCallExpression(states, rules):
    state = states.pop()
    rule = rules[state]
    assert rule.LHS.value == "FunctionCall", "unexpected LHS {}".format(rule.LHS.value)
    if "FunctionCallArgumentList" in [token.value for token in rule.RHS]:
        arguments = parseFunctionCallArgumentList(states, rules)
    else:
        arguments = []
    ref = parseExpression(states, rules)
    return FunctionCallExpression(ref, arguments)
    raise Exception("unexpected state {}".format(state))

def parseFunctionCallArgumentList(states, rules):
    state = states.pop()
    rule = rules[state]
    assert rule.LHS.value == "FunctionCallArgumentList", "unexpected LHS {}".format(rule.LHS.value)
    if len(rule.RHS) == 1:
        rest = []
    else:
        rest = parseFunctionCallArgumentList(states, rules)
    first = [parseExpression(states, rules)]
    return first + rest

def parseBinaryOperator(states, rules):
    state = states.pop()
    rule = rules[state]
    assert rule.LHS.value == "BinaryOperator", "unexpected LHS {}".format(rule.LHS.value)
    op = "".join(terminal.value for terminal in rule.RHS)
    if op == "EQUALS": op = "=="
    return BinaryOperator(op)

def parseValue(states, rules):
    state = states.pop()
    rule = rules[state]
    assert rule.LHS.value == "Value", "unexpected LHS {}".format(rule.LHS.value)    
    if rule.RHS[0].value == "Identifier":
        return parseIdentifier(states, rules)
    if rule.RHS[0].value == "Number":
        return parseNumber(states, rules)
    if rule.RHS[0].value == "StringLiteral":
        return parseStringLiteral(states, rules)
    raise Exception("unexpected state {}".format(state))

def parseIdentifier(states, rules):
    state = states.pop()
    rule = rules[state]
    assert rule.LHS.value == "Identifier", "unexpected LHS {}".format(rule.LHS.value)    
    if len(rule.RHS) == 1:
        return Identifier(parseLetter(states, rules))
    if len(rule.RHS) == 2:
        rest = parseIdentifier(states, rules).id
        first = parseLetter(states, rules)
        return Identifier(first + rest)
    raise Exception("unexpected state {}".format(state))

def parseNumber(states, rules):
    state = states.pop()
    rule = rules[state]
    assert rule.LHS.value == "Number", "unexpected LHS {}".format(rule.LHS.value)    
    if len(rule.RHS) == 1:
        return Number(parseDigit(states, rules))
    if len(rule.RHS) == 2:
        rest = parseNumber(states, rules).num
        first = parseDigit(states, rules)
        return Number(first + rest)
    raise Exception("unexpected state {}".format(state))

#returns a String because I'm too lazy to make a StringLiteral class or whatever.
def parseStringLiteral(states, rules):
    state = states.pop()
    rule = rules[state]
    assert rule.LHS.value == "StringLiteral", "unexpected LHS {}".format(rule.LHS.value)    
    if "CharacterStream" not in [token.value for token in rule.RHS]:
        return StringLiteral("")
    else:
        msg = parseCharacterStream(states, rules)
        return StringLiteral(msg)

#returns a string
def parseCharacterStream(states, rules):
    state = states.pop()
    rule = rules[state]
    assert rule.LHS.value == "CharacterStream", "unexpected LHS {}".format(rule.LHS.value)    
    rest = ""
    if len(rule.RHS) > 1:
        rest = parseCharacterStream(states, rules)
    first = parseCharacter(states, rules)
    return first + rest

def parseCharacter(states, rules):
    state = states.pop()
    rule = rules[state]
    assert rule.LHS.value == "Character", "unexpected LHS {}".format(rule.LHS.value)    
    return rule.RHS[0].value

def parseLetter(states, rules):
    state = states.pop()
    rule = rules[state]
    assert rule.LHS.value == "Letter", "unexpected LHS {}".format(rule.LHS.value)
    return rule.RHS[0].value

def parseDigit(states, rules):
    state = states.pop()
    rule = rules[state]
    assert rule.LHS.value == "Digit", "unexpected LHS {}".format(rule.LHS.value)    
    return rule.RHS[0].value

def interpret(rightDerivation, rules):
    symbols = Stack()
    symbols.data = rightDerivation
    tree = parseStatementList(symbols, rules)
    tree.eval([{}])