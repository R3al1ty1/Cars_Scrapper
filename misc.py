import os

def isHostUp(hostname):
    return os.system("ping -c 1 -t 100 " + hostname + " > /dev/null") == 0