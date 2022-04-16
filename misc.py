import os

def isHostUp(hostname):
    return os.system("ping -c 1 -t 100 " + hostname + " > /dev/null") == 0

def deCamel(inp:str):
    output = ""
    for letter in inp:
        if letter.isupper():
            output += " " + letter.lower()
        else:
            output += letter
    return output