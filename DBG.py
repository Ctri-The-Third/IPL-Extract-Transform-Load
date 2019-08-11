import os
import colorama
from colorama import Fore
from ConfigHelper import getConfig 

def DBG(STR,Level):

    if (Level == 3):
        print("%sDBG: [%s] %s" % (Fore.GREEN, STR, Fore.WHITE) )
    if (Level == 2):
        print("%sDBG: [%s] %s" % (Fore.YELLOW, STR, Fore.WHITE) )
    if (Level == 1):
        print("%sDBG: [%s] %s" % (Fore.RED, STR, Fore.WHITE) )
