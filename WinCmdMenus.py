#queue
#colorama

from DBG import DBG
import os
import time
import colorama
import threading

import queue
#import Queue as queue #python2.7 handling? 
from console import fg, bg, fx 

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
import InputReader
import feedbackQueue # shared module that contains a queue for giving output to the UI

import FetchAchievements 
import BuildMonthlyScoresToJSON 
import BuildMonthlyStarQualityToJSON
import BuildAchievementScoresToJSON
import BuildPlayerBlob
import BuildHeadToHeadsToJSON 
import workerProgressQueue 
# This application class serves as a wrapper for the initialization of curses
# and also manages the actual forms of the application



feedback = []
threads = []

###  https://rosettacode.org/wiki/Terminal_control/Cursor_positioning#Python ###



class COORD(Structure):
    pass
STD_OUTPUT_HANDLE = -11
COORD._fields_ = [("X", c_short), ("Y", c_short)]

def print_at(r, c, s):
    h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    windll.kernel32.SetConsoleCursorPosition(h, COORD(c, r))
    s = s + " "*30
    c = s.encode("windows-1252")
    windll.kernel32.WriteConsoleA(h, c_char_p(c), len(c), None, None)
### END  https://rosettacode.org/wiki/Terminal_control/Cursor_positioning#Python ###



def drawHeader():
    arenaHealth = QueryArena.healthCheck(cfg.getConfigString("SiteNameReal"))
    healthNotice = ["%s%s" % (bg.black,fg.green),"%s%s"% (bg.black,fg.yellow),"%s%s"% (bg.red,fg.black)]
    print_at (0,0,"%s/***** LF Profiler **************************************************\ %s" % (fg.yellow, fg.white))

    outStr  = "Start Date:           [ %s%s%s ]          | " % ( fg.green,  cfg.getConfigString("StartDate"), fg.white)
    outStr = outStr + renderBar((CurrentWorkerStatus["CurEntry"]/CurrentWorkerStatus["TotalEntries"]),fg.black,bg.green)
    print_at(1,0,outStr)
    outStr = "End Date:             [ %s%s%s ]          | " % ( fg.green, cfg.getConfigString("EndDate"),fg.white)
    outStr = outStr + CurrentWorkerStatus["CurrentAction"]
    print_at(2,0,outStr)

    outStr = "Target site:          [ %s%s%s%s ]| " % (healthNotice[arenaHealth],(cfg.getConfigString("SiteNameShort")+ " "*20)[0:20],bg.black,fg.white) 
    
    outStr = outStr + "%s" % (CurrentWorkerStatus["ETA"]) 
    print_at (3,0,outStr)
    print_at (4,0,"")

def drawDateMenu():
    os.system('CLS')
    config = getConfig()
    drawHeader()

    print_at (5,0, "%s/***** Start Date ***************************************************\%s" % (fg.yellow, fg.white))
    print_at (6,0,"%s In the form YYYY-MM-DD       %s" % (fg.yellow, fg.white))
    print_at (7,0,"%s or 'x' to go back            %s" % (fg.yellow, fg.white))
    print_at (8,0,"")
    return input("Enter Start Date: ")
def drawMainMenu():
    #time.sleep(0.05)
    emptyString = "                           "
    inputS = ""
    
    

    drawHeader()

    print_at (5,0,"%s/***** Menu *********************************************************\ %s" % (fg.yellow, fg.white))
    print_at (6,0,"["+fg.yellow+"11 "+fg.white+"] Select different site")
    print_at (7,0,"["+fg.yellow+"12 "+fg.white+"] Select different dates")
    print_at (8,0,"["+fg.yellow+" 4 "+fg.white+"] Run status queries on current site")
    print_at (9,0,"["+fg.yellow+" 5 "+fg.white+"] Run queries on specific player")
    print_at (10,0,"["+fg.yellow+" 6 "+fg.white+"] Rebuild the JSON blobs")
    print_at (11,0,"["+fg.yellow+"61 "+fg.white+"] Update individual player")
    print_at (12,0,"["+fg.yellow+"66 "+fg.white+"] Run DB game search for %sactive%s players at %ssite%s" % (Fore.GREEN,Fore.WHITE,Fore.GREEN, Fore.WHITE))
    print_at (13,0,"["+fg.yellow+"67 "+fg.white+"] Run Achievement refresh for %sall%s %srecent%s players" % (Fore.RED, Fore.WHITE,Fore.GREEN, Fore.WHITE))
    print_at (14,0,"["+fg.yellow+"661"+fg.white+"] Run DB game search for %sall inactivate%s players" % (Fore.RED, Fore.WHITE))
    print_at (15,0,"["+fg.yellow+"666"+fg.white+"] Run DB summary refresh for %sall%s players"% (Fore.RED, Fore.WHITE))
    print_at (16,0,"["+fg.yellow+"667"+fg.white+"] Find %snew%s players for active %ssite%s"% (Fore.RED, Fore.WHITE, Fore.GREEN,Fore.WHITE))
    
    print_at (17,0,"" )
    print_at (18,0,"[?] Help " )
    print_at (19,0,"[x] Exit")
    
    print("")
    
    if feedback.__len__() > 5:
        print ("%s/***** Previous commands *********************************************\%s" % (fg.yellow, fg.white))
        for var in feedback[-5:]:
            var = var + " " * 70 
            var = var[0:70] 
            print("%s%s%s%s%s" % (bg.green,fg.black,var,bg.black, fg.white))

        
    elif feedback.__len__() != 0:
        print ("%s/***** Previous commands ***** %s" % (fg.yellow, fg.white))
        for var in feedback:
            var = var + " " * 70 
            var = var[0:70] 
            print("%s%s%s%s%s" % (bg.green,fg.black,var,bg.black, fg.white))

    
    #print (preS)
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

t = threading.Thread(target=InputReader.executeKeyboardLoop)
threads.append(t)
t.start()    


    
DBG("Startup - menu",3)
os.system('CLS')
waitingFunction = ""
workerStatusQ = workerProgressQueue.getQ()
while inputS != "exit" and inputS != "x": 
    
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
            os.system("cls") #TODO replace this by having the Menu be drawn better.        
        else: 
            drawHeader()
            drawOutputPane()

    elif waitingFunction == "": #The user is in the root menu
        drawMainMenu()
        if inputS == "11":
            waitingFunction = "11"
            os.system("cls")
        if inputS == "12": #needs reworking
            startDate = drawDateMenu()
            print ("%s ***** End Date         ***** %s" % (fg.yellow, fg.white))
            #EndDate = input()

            if startDate != "B" and EndDate != "B":
                feedback.append(setNewDates(startDate,EndDate))
        if inputS == "4": 
            waitingFunction = "outputPane"
        elif inputS == "5":
            waitingFunction = "5"
        elif inputS == "6":
            
            BuildMonthlyScoresToJSON.executeMonthlyScoresBuild()
            BuildMonthlyStarQualityToJSON.executeBuildMonthlyStars()
            BuildAchievementScoresToJSON.executeAchievementBuild()
            BuildPlayerBlob.executeBuildPlayerBlobs()
            BuildHeadToHeadsToJSON.buildHeadToHeads() 
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
            os.system("cls")
            waitingFunction = ""
    else: 
        drawHeader()
        drawOutputPane()
    time.sleep(.5)





