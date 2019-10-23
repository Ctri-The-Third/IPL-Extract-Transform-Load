import time
import queue
import math


q = queue.Queue()
WorkerStatus = {}
WorkerStatus["CurEntry"] = 0
WorkerStatus["TotalEntries"] = 1
WorkerStatus["CurrentAction"] = "[        idle        ]" 
WorkerStatus["ETA"] = "[      ETC: N/A      ]" 

q.put(WorkerStatus)

def updateQ(curEntry,total,action,ETA):
    WorkerStatus = {}
    WorkerStatus["CurEntry"] = curEntry
    WorkerStatus["TotalEntries"] = total

    action = action[0:20]
    paddingL = math.floor(10 - (len(action)/2))
    paddingR = math.ceil(10 - (len(action)/2))
    action = "[%s%s%s]" % (" " * paddingL,action," " * paddingR)
    WorkerStatus["CurrentAction"] = action 

    paddingL = math.floor(10 - (len(ETA)/2))
    paddingR = math.ceil(10 - (len(ETA)/2))
    ETA = "[%s%s%s]" % (" " * paddingL,ETA," " * paddingR)
    WorkerStatus["ETA"] = ETA 

    global q 
    q.put(WorkerStatus)
def getQ():
    return q