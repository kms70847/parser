#converts a string into an array of rules.
#example input:
"""\
S -> Expression
Expression -> Expression * Binary
Expression -> Expression + Binary
Expression -> Binary
Binary -> 0
Binary -> 1"""


from primitives import *

def parseRules(ruleText):
    ret = []
    lines = ruleText.split("\n")
    #remove comments and trailing whitespace
    lines = [line.partition("#")[0].strip() for line in lines]
    #filter out empty lines
    lines = [line for line in lines if len(line) > 1]
    #expand lines of the form "A -> B | C" into two lines, "A -> B" and "A -> C"
    expandedLines = []
    for line in lines:
        if "|" in line:
            LHS, RHSs = line.split("->")
            for RHS in RHSs.split("|"):
                RHS = RHS.strip()
                expandedLines.append(LHS + "->" + RHS)
        else:
            expandedLines.append(line)
    lines = expandedLines

    nonTerminalSymbols = set(map(lambda x: x.split("->")[0].strip(), lines))
    if "_" not in nonTerminalSymbols:
        print "Warning, expected starting Symbol _"
    for line in lines:
        line = line.split("->")
        LHS = NonTerminal(line[0].strip())
        RHS = []
        for token in line[1].split():
            if token == "%SPACE%": token = " "
            if token in nonTerminalSymbols:
                RHS.append(NonTerminal(token))
            else:
                #breaking up terminal tokens into individual characters is a double-edged sword.
                #it makes tokenizing as simple as iterating a string,
                #but it increases the size of the parsing table,
                #and potentially increases the likelihood of shift-reduce collisions. (?)
                for char in token:
                    RHS.append(Terminal(char))
        ret.append(Rule(LHS, RHS))
    return ret

#old version of parseRules. Only allows symbols one character long, and spaces are treated as terminals.
#example input:
"""S->E
E->E*B
E->E+B
E->B
B->0
B->1"""
def _parseRules(ruleText):
    ret = []
    lines = ruleText.split("\n")
    nonTerminalSymbols = map(lambda x: x.split("->")[0], lines)
    for line in lines:
        line = line.split("->")
        LHS = NonTerminal(line[0])
        RHS = []
        for char in line[1]:
            if char in nonTerminalSymbols:
                RHS.append(NonTerminal(char))
            else:
                RHS.append(Terminal(char))
        ret.append(Rule(LHS, RHS))
    return ret