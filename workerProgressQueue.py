import time
import queue
import math
from  colorama import Fore,Back

q = queue.Queue()
WorkerStatus = {}
WorkerStatus["CurEntry"] = 0
WorkerStatus["TotalEntries"] = 1
WorkerStatus["CurrentAction"] = "[%s        idle        %s]" % (Fore.GREEN, Fore.WHITE)
WorkerStatus["ETA"] = "[%s      ETC: N/A      %s]" % (Fore.GREEN, Fore.WHITE)

q.put(WorkerStatus)

def updateQ(curEntry,total,action,ETA):
    WorkerStatus = {}
    WorkerStatus["CurEntry"] = curEntry
    WorkerStatus["TotalEntries"] = total

    action = action[0:20]
    paddingL = math.floor(10 - (len(action)/2))
    paddingR = math.ceil(10 - (len(action)/2))
    action = "[%s%s%s%s%s]" % (Fore.GREEN," " * paddingL,action," " * paddingR,Fore.WHITE)
    WorkerStatus["CurrentAction"] = action 

    paddingL = math.floor(10 - (len(ETA)/2))
    paddingR = math.ceil(10 - (len(ETA)/2))
    ETA = "[%s%s%s%s%s]" % (Fore.GREEN," " * paddingL,ETA," " * paddingR,Fore.WHITE)
    WorkerStatus["ETA"] = ETA 

    global q 
    q.put(WorkerStatus)
def getQ():
    return q