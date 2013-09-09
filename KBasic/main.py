#ugly stuff to import modules one directory up
import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir) 

from util import constructParser
from interpreter import interpret
from parseRules import parseRules

def slurp(filename):
    file = open(filename)
    rulesText = file.read()
    file.close()
    return rulesText

def tokenizeProgram(data):
    lines = data.split("\n")
    #remove comments
    lines = [line.partition("#")[0] for line in lines]
    characters = []
    inString = False
    for char in "".join(lines):
        if char == "\"":
            inString = not inString
        if char == " " and not inString: continue
        if char == "\t" and not inString: continue
        characters.append(char)
    return "".join(characters)

rulesText = slurp("language.txt")
rules = parseRules(rulesText)
programText = tokenizeProgram(slurp("test.k"))



parser = constructParser(rulesText)
rightDerivation = parser.parse(programText)

#print "result of {}:".format(programText)
interpret(rightDerivation, rules)