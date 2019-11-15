import feedbackQueue
import os
import colorama
from colorama import Fore
import datetime



#3 = Info
#2 = Warning
#1 = Error
def DBG(STR,Level=1):
    if Level < 0 or Level > 3:
        Level = 1
    if (Level == 3):
        outStr = "%sDBG: [%s] %s" % (Fore.GREEN, STR, Fore.WHITE) 
    if (Level == 2):
        outStr = "%sDBG: [%s] %s" % (Fore.YELLOW, STR, Fore.WHITE) 
    if (Level == 1):
        outStr = "%sDBG: [%s] %s" % (Fore.RED, STR, Fore.WHITE) 

    #print(outStr)
    if Level <= 2:
        feedbackQueue.q.put(outStr)
    f = open("DBG.log","a+")
    loggingLevels = ["[ERROR]  ","[WARNING]","[INFO]   "]
    f.write("%s [%s]\t %s\n" % (loggingLevels[Level-1],str(datetime.datetime.now()),STR))
    f.close()