#ugly stuff to import modules one directory up
import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir) 

from util import constructParser
from interpreter import interpret

def loadRules(filename):
    file = open(filename)
    rulesText = file.read()
    file.close()
    return rulesText

rulesText = loadRules("language.txt")
programText = "1+1*1+1"

parser = constructParser(rulesText)
rightDerivation = parser.parse(programText)

print "result of {}:".format(programText)
print interpret(rightDerivation)