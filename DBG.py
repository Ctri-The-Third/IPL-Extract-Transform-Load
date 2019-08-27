import feedbackQueue
import os
import colorama
from colorama import Fore




def DBG(STR,Level):

    if (Level == 3):
        outStr = "%sDBG: [%s] %s" % (Fore.GREEN, STR, Fore.WHITE) 
    if (Level == 2):
        outStr = "%sDBG: [%s] %s" % (Fore.YELLOW, STR, Fore.WHITE) 
    if (Level == 1):
        outStr = "%sDBG: [%s] %s" % (Fore.RED, STR, Fore.WHITE) 

    print(outStr)
    if Level <= 2:
        feedbackQueue.q.put(outStr)
