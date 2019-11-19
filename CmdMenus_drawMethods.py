from DBG import DBG
import os


if os.name == "nt":
    from WinCmdMenus import * 
elif os.name == "posix":
    from LinuxCmdMenus import *
    

import time
import threading
import feedbackQueue


from renderProgressBar import renderBar
import ConfigHelper as cfg 
import QueryArena
from workerProgressQueue import *

from SQLHelper import getActiveJobs

# This application class serves as a wrapper for the initialization of curses
# and also manages the actual forms of the application

#`P`ALLETE
# 0 = White on black
# 1 = Green on Black
# 2 = Yellow on Black
# 3 = Red on Black
# 4 = Black on Green
# 5 = Black on Red

 

def drawHeader(CurrentWorkerStatus, threadcounter):
    arenaHealth = QueryArena.healthCheck(cfg.getConfigString("SiteNameReal"))
    
    print_at (0,0,"/----- LF Profiler --------------------------------------------------\\ ",PI=2)
         
    print_at(1,0,"Dates:  [            ] to [            ]      | " )
    print_at(1,10,cfg.getConfigString("StartDate"),1)
    print_at(1,28,cfg.getConfigString("EndDate"),1) 
    renderBar((CurrentWorkerStatus["CurEntry"]/CurrentWorkerStatus["TotalEntries"]),1,48,4,1)
    
    print_at(2,0,"Target site:     [                     ]      |  ")
    print_at(2,19,(cfg.getConfigString("SiteNameShort")+ " "*20)[0:20],arenaHealth+1)
    print_at(2,48,CurrentWorkerStatus["CurrentAction"],1)

    print_at(3,0,"active threads:           [            ]      | " )
    if threadcounter < 4:
        threadColour = 1
    elif threadcounter < 8:
        threadColour = 2
    else:
        threadColour = 3
    print_at(3,28,"%s threads"[:10] % threadcounter,threadColour) 
    print_at(3,48,"%s"%(CurrentWorkerStatus["ETA"]),1)
    
    #1print_at (3,0,outStr)
    print_at (4,0,"") 

def drawDateMenu(CurrentWorkerStatus,threadCounter):
    os.system('CLS')
    drawHeader(CurrentWorkerStatus,threadCounter)
 
    print_at (5,0, "/***** Start Date ***************************************************\\" ,PI=2 )
    print_at (6,0,"In the form YYYY-MM-DD       ",PI=2)
    print_at (7,0,"or 'x' to go back            ",PI=2)
    print_at (8,0,"")
    return input("Enter Start Date: ")
def drawMainMenu(CurrentWorkerStatus,threadCounter,feedback, stayActiveFlag):
    #time.sleep(0.05)

    drawHeader(CurrentWorkerStatus,threadCounter)
    
    print_at (5,0, "/----- Menu ---------------------------------------------------------\\ " ,PI=2 )
    print_at (6,0,"[11 ] Select different site")
    print_at (7,0,"[12 ] Select different dates")
    print_at (8,0,"[4  ] Run status queries on current site")
    print_at (8,1,"4",PI=1)
    print_at (9,0,"[5  ] Run queries on specific player")
    print_at (9,1,"5",PI=1)
    print_at (10,0,"[6  ] Rebuild the JSON blobs")
    print_at (10,1,"6",PI=2)
    print_at (11,0,"[61 ] Update individual player")
    print_at (11,1,"61",PI=1)
    print_at (12,0,"[66 ] Run DB game search for active players at site")
    print_at (12,1,"66",PI=1)
    print_at (13,0,"[67 ] Run Achievement refresh for all recent players")
    print_at (13,1,"67",PI=2)
    print_at (14,0,"[677] Run Achievement refresh for all active players")
    print_at (14,1,"677",PI=3)
    print_at (15,0,"[661] Run DB game search for all inactivate players" )
    print_at (15,1,"661",PI=3)
    print_at (16,0,"[666] Run DB summary refresh for all players")
    print_at (16,1,"666",PI=3)
    print_at (17,0,"[667] Find new players for active site")
    print_at (17,1,"667",PI=2)
    
    print_at (18,0,"" )
    print_at (19,0,"[t] threads \t[x] Exit" )
    if stayActiveFlag:
        print_at(19,30,"[s] re-enable auto-shutdown")
    else: 
        print_at(19,30,"[s] disable auto-shutdown")
    print_at (20,0,"")
    
    
    
    if feedback.__len__() >= 5:
        print_at (21,0,"/----- Previous commands ---------------------------------------------\\ ",PI=2)
        counter = 0 
        for var in feedback[-5:]:
            counter = counter + 1
            var = var + " " * 70 
            var = var[0:70] 
            print_at(21+counter,0,var,PI=4)

        
def drawArenaMenu():
    counter = 5
    print_at (5,0,"/***** Pick arena ***************************************************\\",PI=2)
    for arena in cfg.getConfigString("configs"):
        counter = counter + 1 
        print_at (counter,0,"[%i] %s" % (counter -5 ,arena["SiteNameShort"]))
    


def drawOutputPane(feedback):
    counter = 0
    print_at (5,0,"/***** Output ******************************************************\\", PI=2)
    for var in feedback[-15:]:
        var = var + " " * 70 
        var = var[0:100] 
        counter = counter + 1
        print_at(5+counter,0,var,PI=4)
    if len(feedback) < 15:
        for i in range(15 - len(feedback)):
            print_at(5+counter+i+1,0," " * 70)


 
_lastTcounter = 0
_lastJcounter = 0
def drawJobsAndThreads(threads):
    global _lastTcounter
    global _lastJcounter
    tCounter = 1
    print_at (5,0,"/***** Threads! *****************************************************\\", PI=2)
    for t in threads:
        if t.isAlive():
            print_at (5+tCounter,0,"%s: %s" % (tCounter, t.name))
            tCounter = tCounter + 1
    jobs = getActiveJobs()
    jCounter = 1
     
    print_at (5+tCounter+jCounter,0,"/***** Jobs! ********************************************************\\",PI=2)
    try:
        if len(jobs) == 0:
            print_at(7+tCounter+jCounter,0,"No active jobs found! System is quiescent.")
        else: 
            for j in jobs:
                health = ("%s" % (j[1],)+" "*10)[:10]
                description = ("%s"%(j[3])+" "*30)[:30]
                if j[1] != "complete":
                    percent = ("%s%%" % (j[11])+" "*10)[:10]
                    if j[3] > 1000:
                        ageSuff = "K"
                        j[3] = j[3] / 1000
                        if j[3] > 1000:
                            ageSuff = "M"
                            j[3] = j[3] / 1000
                            if j[3] > 1000:
                                ageSuff = "B"
                                j[3] = j[3] / 1000
                                if j[3] > 1000:
                                    ageSuff = "∞"
                                    j[3] = j[3] / 1000 



 
                else:
                    percent = "100.000%"
                    ageSuff = "∞"
                
                if ageSuff != "∞":
                    ageStr = "%s"%(math.trunc(j[3]))
                    ageStr = "%s"%(ageStr[3:],ageSuff) 
                else:
                    ageStr = "∞   "
                print_at (6+tCounter+jCounter,0,"%s %s\t%s: %s\t%s" % (ageStr,health,j[4][3:],description,percent) )
                jCounter = jCounter + 1 
        
        if tCounter != _lastTcounter or jCounter != _lastJcounter:
            _lastJcounter = jCounter
            _lastTcounter = tCounter
            clearScreen()

    except:
        pass   
    print_at(8+tCounter+jCounter,0,"enter 'a' to continue...")

_safeShutdownCheckLast = time.time()
def safeShutdownCheck(threads,lastInput,overrideFlag = False):
    global _safeShutdownCheckLast
    if (time.time() -_safeShutdownCheckLast) / 60 > 1:
        _safeShutdownCheckLast = time.time()            
        doWeShutDown = True
        if len(threads) > 3:
            doWeShutDown = False

        currentTime = time.time() - lastInput
        if currentTime/60 < 20:
            doWeShutDown = False
        if len(getActiveJobs()) > 3:
            doWeShutDown = False

        if overrideFlag:
            doWeShutDown = False
        #any active threads? 
        #MAIN
        #Heartbeat
        #Input/Render

        #any incomplete jobs?

        #any manual activity in the last 20 minutes?

        #any override to prevent shutdown?
        return doWeShutDown
    else:
        return False