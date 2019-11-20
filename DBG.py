"""Output a debug string to the UI and the console, with colours for the severity.
Severity 1 = red / error
Severity 2 = Yellow / Warning
Severity 3 = green / info"""

import feedbackQueue
import os 
import datetime
import threading


#3 = Info
#2 = Warning
#1 = Error 
def DBG(STR,Level=1):
    if Level < 0 or Level > 3:
        Level = 1
    if (Level == 3):
        outStr = "DBG: [%s] " % (STR) 
    if (Level == 2):
        outStr = "DBG: [%s] " % (STR) 
    if (Level == 1):
        outStr = "DBG: [%s] " % (STR) 

    #print(outStr)
    if Level <= 2:
        feedbackQueue.q.put(outStr)
    f = open("DBG.log","a+")
    loggingLevels = ["[ERROR]  ","[WARNING]","[INFO]   "]
    f.write("%s [%s]\t%s \t%s\n" % (loggingLevels[Level-1],str(datetime.datetime.now()),threading.get_ident(),STR))
    f.close()