from DBG import DBG
import os


if os.name == "nt":
    from WinCmdMenus import * 
elif os.name == "posix":
    from LinuxCmdMenus import *
    

#queue
#colorama


import time
import colorama
import threading

import queue
#import Queue as queue #python2.7 handling? 


from renderProgressBar import renderBar
from colorama import Fore
from colorama import Back
import ConfigHelper as cfg 
from ctypes import *

from FetchPlayerAndGames import executeQueryGames
from FetchPlayerUpdatesAndNewPlayers import updateExistingPlayers
from FetchPlayerUpdatesAndNewPlayers import findNewPlayers
from FetchAchievements import executeFetchAchievements
import FetchPlayerAndGames
import FetchPlayerUpdatesAndNewPlayers
import FetchIndividual 
import QueryIndividual
import QueryArena

import feedbackQueue # shared module that contains a queue for giving output to the UI

import FetchAchievements 
import InputReader

import BuildMonthlyScoresToJSON 
import BuildMonthlyStarQualityToJSON
import BuildAchievementScoresToJSON
import BuildPlayerBlob
import BuildHeadToHeadsToJSON 
import workerProgressQueue 
# This application class serves as a wrapper for the initialization of curses
# and also manages the actual forms of the application

initUI()
#PALLETE
# 0 = White on black
# 1 = Green on Black
# 2 = Yellow on Black
# 3 = Red on Black
# 4 = Black on Green
# 5 = Black on Red

feedback = ["","","","","Initialised system..."]
threads = []


 

def drawHeader():
    arenaHealth = QueryArena.healthCheck(cfg.getConfigString("SiteNameReal"))
    
    print_at (0,0,"/***** LF Profiler **************************************************\ ",PI=2)

         
    
    
    print_at(1,0,"Start Date:           [            ]          | " )
    print_at(1,24,cfg.getConfigString("StartDate"),1)
    renderBar((CurrentWorkerStatus["CurEntry"]/CurrentWorkerStatus["TotalEntries"]),1,48,4,1)
    
    
    print_at(2,0,"Start Date:           [            ]          | " )
    print_at(2,24,cfg.getConfigString("StartDate"),1) 
    print_at(2,48,CurrentWorkerStatus["CurrentAction"],1)
    

    print_at(3,0,"Target site:          [                     ] |  ")

    print_at(3,24,(cfg.getConfigString("SiteNameShort")+ " "*20)[0:20],arenaHealth+1)
    print_at(3,48,"%s"%(CurrentWorkerStatus["ETA"]),1)
    #1print_at (3,0,outStr)
    print_at (4,0,"") 

def drawDateMenu():
    os.system('CLS')
    config = cfg.getConfig()
    drawHeader()
 
    print_at (5,0, "/***** Start Date ***************************************************\ " ,PI=2 )
    print_at (6,0,"%s In the form YYYY-MM-DD       %s" % (fg.yellow, fg.white))
    print_at (7,0,"%s or 'x' to go back            %s" % (fg.yellow, fg.white))
    print_at (8,0,"")
    return input("Enter Start Date: ")
def drawMainMenu():
    #time.sleep(0.05)
    emptyString = "                           "
    inputS = ""
    
    

    drawHeader()

    print_at (5,0,"/***** Menu *********************************************************\ ",PI=2)
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
    print_at (13,1,"67",PI=3)
    print_at (14,0,"[661] Run DB game search for all inactivate players" )
    print_at (14,1,"661",PI=3)
    print_at (15,0,"[666] Run DB summary refresh for all players")
    print_at (15,1,"666",PI=3)
    print_at (16,0,"[667] Find new players for active site")
    print_at (16,1,"667",PI=2)
    
    print_at (17,0,"" )
    print_at (18,0,"[?] Help " )
    print_at (19,0,"[x] Exit")
    
    
    
    if feedback.__len__() >= 5:
        print_at (21,0,"/***** Previous commands *********************************************\ ",PI=2)
        counter = 0 
        for var in feedback[-5:]:
            counter = counter + 1
            var = var + " " * 70 
            var = var[0:70] 
            print_at(21+counter,0,var,PI=4)

        
def drawArenaMenu():
    global config
    counter = 5
    print_at (5,0,"%s/***** Pick arena ***************************************************\ %s" % (fg.yellow, fg.white))
    for arena in cfg.getConfigString("configs"):
        counter = counter + 1 
        print_at (counter,0,"[%s%i%s] %s" % (Fore.YELLOW,counter -5 ,Fore.WHITE,arena["SiteNameShort"]))
    counter = counter + 1
    print_at (counter,0,"[%sB%s] Return to main menu" % (Fore.YELLOW, Fore.WHITE))
    


def drawOutputPane():
    counter = 0
    print_at (5,0,"%s/***** Output ******************************************************\%s" % (fg.yellow, fg.white))
    for var in feedback[-15:]:
        var = var + " " * 70 
        var = var[0:100] 
        counter = counter + 1
        print_at(5+counter,0,("%s%s%s%s%s" % (bg.green,fg.black,var,bg.black, fg.white)))
    if len(feedback) < 15:
        for i in range(15 - len(feedback)):
            print_at(5+counter+i+1,0," " * 70)


preS = "" 
inputS = ""


t = startInputThread()
threads.append(t) 


    
DBG("Startup - menu",3)
clearScreen()
waitingFunction = ""
workerStatusQ = workerProgressQueue.getQ()

#rendering is done generically, but the wrapper and refresh must be handled by the CmdMenus part.
stop = False
while inputS != "exit" and inputS != "x" and stop != True:
    time.sleep(0.5)
    print_at(0,0,"LOOP [%s]"% stop)
    inputS = ""
    while not feedbackQueue.q.empty():
        feedback.append(feedbackQueue.q.get())
    while not InputReader.q.empty():
        inputS = InputReader.q.get()
        feedback.append(inputS)


        
    
    if not workerStatusQ.empty():    
        CurrentWorkerStatus = workerStatusQ.get() #fetch the latest update
        workerStatusQ.queue.clear() #purge older updates
    

    #print(CurrentWorkerStatus)
    #currently prioritise minor update over major update
    
    if waitingFunction == "11":
        
        drawHeader()
        drawArenaMenu()
        #print("\nEnter option...")
        if inputS != "":
            if inputS == "b":
                waitingFunction = ""
                
            else:
                cfg.setActive(int(inputS)-1)
                waitingFunction = ""
                

    elif waitingFunction == "61" and inputS != '':
        
        drawHeader()
        drawOutputPane()
        FetchIndividual.fetchIndividualWithID(inputS)
        feedbackQueue.q.put("Enter A to continue...")
        waitingFunction = "outputPane"
        
    elif waitingFunction == "5":
        if inputS != '':
            drawHeader()
            drawOutputPane()
            QueryIndividual.executeQueryIndividual(inputS)
            feedbackQueue.q.put("Enter A to continue...")
            waitingFunction = "outputPane"
    elif waitingFunction == "outputPane":
        if inputS == 'a':
            waitingFunction = ""
            clearScreen() #TODO replace this by having the Menu be drawn better.        
        else: 
            drawHeader()
            drawOutputPane()

    elif waitingFunction == "": #The user is in the root menu
        drawMainMenu()
        if inputS == "11":
            waitingFunction = "11"
            clearScreen()
        if inputS == "12": #needs reworking
            startDate = drawDateMenu()
            print ("%s ***** End Date         ***** %s" % (fg.yellow, fg.white))
            EndDate = input("Enter End Date:")

            if startDate != "B" and EndDate != "B":
                feedback.append(cfg.setNewDates(startDate,EndDate))
        if inputS == "4": 
            waitingFunction = "outputPane"
        elif inputS == "5":
            waitingFunction = "5"
        elif inputS == "6":
            
            feedback.append("Building all blobs in parallel. Prepare for spam.")
            t = threading.Thread(target=BuildMonthlyScoresToJSON.executeMonthlyScoresBuild())
            threads.append(t)
            t.start() 

            t = threading.Thread(target=BuildMonthlyStarQualityToJSON.executeBuildMonthlyStars())
            threads.append(t)
            t.start()

            t = threading.Thread(target=BuildAchievementScoresToJSON.executeAchievementBuild())
            threads.append(t)
            t.start()

            t = threading.Thread(target=BuildPlayerBlob.executeBuildPlayerBlobs())
            threads.append(t)
            t.start()

            t = threading.Thread(target=BuildHeadToHeadsToJSON.buildHeadToHeads())
            threads.append(t)
            t.start()

            feedback.append("Blobs written")
            
            

        elif inputS == "61":
            
            waitingFunction = "61"
            feedback.append("Enter User ID or GamerTag to search")
        elif inputS == "66":
            feedback.append("Performing update of active local players in background...")
            t = threading.Thread(target=executeQueryGames, args=("partial",))
            threads.append(t)
            t.start()      
            inputS = ""
        elif inputS == "67":

            feedback.append("Performing background update of achievements for recent players...")
            t = threading.Thread(target=executeFetchAchievements, args =("partial",))
            threads.append(t)
            t.start()      
            inputS = ""

        elif inputS == "661":
            feedback.append("Performing update of inactivate players in background...")
            t = threading.Thread(target=executeQueryGames, args=("full",))
            threads.append(t)
            t.start()      
            inputS = ""
        elif inputS == "666":
            feedback.append("Performing complete update in background...")
            t = threading.Thread(target=updateExistingPlayers)
            threads.append(t)
            t.start()
            inputS = ""
        elif inputS == "667":
            feedback.append("Seeking new players in background...")
            t = threading.Thread(target=findNewPlayers)
            threads.append(t)
            t.start()
            inputS = ""
        elif inputS == "cls":
            feedback.append("Clearing console")
            clearScreen()
            waitingFunction = ""
    else:
        Nothing = True 
        #drawHeader()
        #drawOutputPane()
    drawScreen()
    

endUI()



