#!/usr/bin/env python3
from DBG import DBG
import os
import threadRegistrationQueue as TRQ
 

if os.name == "nt":
    from WinCmdMenus import * 
elif os.name == "posix":
    from LinuxCmdMenus import *
    
#INSTALL PostGresSQL
#Create LaserScraper Database
#Run DBSetup.sql
#queue
#console 
#pynput
#curses


import time
import threading

import queue
#import Queue as queue #python2.7 handling? 
 
from renderProgressBar import renderBar
import ConfigHelper as cfg 
from ctypes import *
from CmdMenus_drawMethods import *
from FetchPlayerAndGames import executeQueryGames
from FetchPlayerUpdatesAndNewPlayers import updateExistingPlayers
from FetchPlayerUpdatesAndNewPlayers import findNewPlayers
from FetchAchievements import executeFetchAchievements
import BuildAllForAllArenasSequentially
import FetchPlayerAndGames
import FetchPlayerUpdatesAndNewPlayers
import FetchIndividual 
import QueryIndividual
import QueryArena 
import periodicFunctions
import feedbackQueue # shared module that contains a queue for giving output to the UI

import FetchAchievements 
import InputReader
import HeartMonitor
import BuildMonthlyScoresToJSON 
import BuildMonthlyStarQualityToJSON
import BuildAchievementScoresToJSON
import BuildPlayerBlob
import BuildHeadToHeadsToJSON 
import BuildAnnualArenaMetrics 
import BuildAnnualTop3s
import workerProgressQueue 
import SQLHelper
# This application class serves as a wrapper for the initialization of curses
# and also manages the actual forms of the application
 
#PALLETE
# 0 = White on black
# 1 = Green on Black
# 2 = Yellow on Black
# 3 = Red on Black
# 4 = Black on Green
# 5 = Black on Red

feedback = ["","","","","Initialised system..."]
threads = []
threadQueue = queue.Queue()
t = threading.currentThread()
threads.append(t)

t = initUI()
if t is not None:
    t.name = "RenderThread"
    threads.append(t)

 

preS = "" 
inputS = ""

def addThread(newThread):
    global threadQueue
    threadQueue.put(newThread)


t = startInputThread() #screen goes black here. Why?
if t is not None: 
    t.name = "inputThread"
    threads.append(t) 

heartMonitor = HeartMonitor.startMonitorThreads()
threads.append(heartMonitor)

    
DBG("Startup - menu",3)
clearScreen()
waitingFunction = ""
workerStatusQ = workerProgressQueue.getQ()

#rendering is done generically, but the wrapper and refresh must be handled by the CmdMenus part.
stop = False
_overrideFlag = False
_lastInput = time.time()
while (inputS != "exit" and inputS != "x" and stop != True) and not safeShutdownCheck(threads,_lastInput,_overrideFlag):
    time.sleep(0.33)
    print_at(0,0,"LOOP [%s]"% stop)
    inputS = ""
    while not feedbackQueue.q.empty():
        feedback.append(feedbackQueue.q.get())
    while not InputReader.q.empty():
        inputS = InputReader.q.get()
        _lastInput = time.time()
        feedback.append(inputS)
    while not TRQ.q.empty():
        threads.append(TRQ.q.get())

         
    
    if not workerStatusQ.empty():    
        CurrentWorkerStatus = workerStatusQ.get() #fetch the latest update
        workerStatusQ.queue.clear() #purge older updates
    threadCounter = 0
    for t in threads:
        if t.isAlive():
            threadCounter = threadCounter + 1
    #print(CurrentWorkerStatus)
    #currently prioritise minor update over major update
    if waitingFunction != "":
        
        if waitingFunction == "t":
            if inputS == 'a':
                waitingFunction = ""

            drawHeader(CurrentWorkerStatus,threadCounter)
            drawJobsAndThreads(threads)
        
        elif waitingFunction == "11":
            
            drawHeader(CurrentWorkerStatus,threadCounter)
            drawArenaMenu()
            #print("\nEnter option...")
            if inputS != "":
                if inputS == "b":
                    waitingFunction = ""
                    
                else:
                    cfg.setActive(int(inputS)-1)
                    waitingFunction = ""
                    

        elif waitingFunction == "61" and inputS != '':
            
            drawHeader(CurrentWorkerStatus,threadCounter)
            drawOutputPane(feedback)
            FetchIndividual.fetchIndividualWithID(inputS)
            feedbackQueue.q.put("Enter A to continue...")
            waitingFunction = "outputPane"
            
        elif waitingFunction == "5":
            if inputS != '':
                drawHeader(CurrentWorkerStatus,threadCounter)
                drawOutputPane(feedback)
                QueryIndividual.executeQueryIndividual(inputS)
                feedbackQueue.q.put("Enter A to continue...")
                waitingFunction = "outputPane"
        elif waitingFunction == "outputPane":
            if inputS == 'a':
                waitingFunction = ""
                clearScreen() #TODO replace this by having the Menu be drawn better.        
            else: 
                drawHeader(CurrentWorkerStatus,threadCounter)
                drawOutputPane(feedback)

    elif waitingFunction == "": #The user is in the root menu
        drawMainMenu(CurrentWorkerStatus,threadCounter,feedback,_overrideFlag)
        if inputS == "11":
            waitingFunction = "11"
            clearScreen()
        if inputS == "12": #needs reworking
            startDate = drawDateMenu(CurrentWorkerStatus,threadCounter)
            print_at (10,1,"LOCATION? ***** End Date         ***** ",PI=2)
            EndDate = input("Enter End Date:")

            if startDate != "B" and EndDate != "B":
                feedback.append(cfg.setNewDates(startDate,EndDate))
        if inputS == "4": 
            waitingFunction = "outputPane"
        elif inputS == "5":
            waitingFunction = "5"
        elif inputS == "6":
            
            feedback.append("Building all blobs in series.")
            t = threading.Thread(target=BuildAllForAllArenasSequentially.buildAllForAllArenasSequentially)
            t.name = "6 - Render all things."
            threads.append(t)
            t.start() 

            

        elif inputS == "61":
            
            waitingFunction = "61"
            feedback.append("Enter User ID or GamerTag to search")
        elif inputS == "66": 
            
            feedback.append("Queuing tasks. Will being in <30 seconds...")
            periodicFunctions.queueWeekly()
            inputS = ""
        elif inputS == "67":
            feedback.append("Performing background update of achievements for recent players...")
            t = threading.Thread(target=executeFetchAchievements, args =("recent",))
            t.name = "67, ach <=7 days"
            threads.append(t)
            t.start()      
            inputS = ""
        elif inputS == "677":
            feedback.append("Performing background update of achievements for active players...")
            t = threading.Thread(target=executeFetchAchievements, args =("partial",))
            t.names = "677 - ach actives"
            threads.append(t)
            t.start()      
            inputS = ""
        elif inputS == "661":
            feedback.append("Performing update of inactivate players in background...")
            t = threading.Thread(target=executeQueryGames, args=("full",))
            t.name = "661 - games, all inactive "
            threads.append(t)
            t.start()      
            inputS = ""
        elif inputS == "666":
            #MONTHLY UPDATE
            feedback.append("Performing complete update in background...")
            periodicFunctions.queueMonthly()
            inputS = ""
        elif inputS == "667":
            feedback.append("Seeking new players in background...")
            t = threading.Thread(target=findNewPlayers)
            t.name = "667, new player search for someone"
            threads.append(t)
            t.start()
            inputS = ""
        elif inputS == "cls":
            feedback.append("Clearing console")
            clearScreen()
            waitingFunction = ""
        elif inputS == "t":
            feedback.append("Opening thread & jobs view")   
            waitingFunction = "t"
            clearScreen()
        elif inputS == "s":
            _overrideFlag = not _overrideFlag

    else:
        Nothing = True 
        #drawHeader(CurrentWorkerStatus,threadCounter)
        #drawOutputPane(feedback)
    drawScreen()
for t in threads:
    t._stop() #hard kill all threads. 
HeartMonitor.terminateMonitor()
endUI()



