import os
import time
import colorama
import threading
import queue 
from console import fg, bg, fx 

from renderProgressBar import renderBar
from colorama import Fore
from colorama import Back
from ConfigHelper import getConfig 
from ConfigHelper import setActive
from ConfigHelper import setNewDates
from ctypes import *

from FetchPlayerAndGames import executeQueryGames
from FetchPlayerUpdatesAndNewPlayers import updateExistingPlayers
import FetchPlayerAndGames
import FetchPlayerUpdatesAndNewPlayers
import FetchIndividual  
import QueryIndividual
import InputReader
import feedbackQueue # shared module that contains a queue for giving output to the UI
 
# This application class serves as a wrapper for the initialization of curses
# and also manages the actual forms of the application


feedback = []
threads = []
config = getConfig()
###  https://rosettacode.org/wiki/Terminal_control/Cursor_positioning#Python ###
class COORD(Structure):
    pass
STD_OUTPUT_HANDLE = -11
COORD._fields_ = [("X", c_short), ("Y", c_short)]
 
def print_at(r, c, s):
    h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    windll.kernel32.SetConsoleCursorPosition(h, COORD(c, r))
 
    c = s.encode("windows-1252")
    windll.kernel32.WriteConsoleA(h, c_char_p(c), len(c), None, None)
### END  https://rosettacode.org/wiki/Terminal_control/Cursor_positioning#Python ###

def drawHeader():

    print_at (0,0,"%s/***** LF Profiler **************************************************\ %s" % (fg.yellow, fg.white))
    config = getConfig()
    outStr  = "Start Date:           [ %s%s%s ]          | " % ( fg.green,  config["StartDate"], fg.white)
    outStr = outStr + renderBar((CurrentWorkerStatus["CurEntry"]/CurrentWorkerStatus["TotalEntries"]),fg.black,bg.green)
    outStr = outStr + "\nEnd Date:             [ %s%s%s ]          | " % ( fg.green, config["EndDate"],fg.white)
    outStr = outStr + CurrentWorkerStatus["CurrentAction"]
    outStr = outStr + "\nTarget site:          [ %s%s%s ]| " % (fg.green,config["SiteNameShort"][0:20],fg.white) 
    outStr = outStr + "%s" % (CurrentWorkerStatus["ETA"]) 
    print_at (1,0,outStr)
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
    
    config = getConfig()

    drawHeader()

    print_at (5,0,"%s/***** Menu *********************************************************\ %s" % (fg.yellow, fg.white))
    print_at (6,0,"["+fg.yellow+"11 "+fg.white+"] Select different site")
    print_at (7,0,"["+fg.yellow+"12 "+fg.white+"] Select different dates")
    print_at (8,0,"["+fg.yellow+" 5 "+fg.white+"] Run queries on specific player")
    print_at (9,0,"["+fg.yellow+" 6 "+fg.white+"] Rebuild the JSON blobs")
    print_at (10,0,"["+fg.yellow+"61 "+fg.white+"] Update individual player")
    print_at (11,0,"["+fg.yellow+"66 "+fg.white+"] Run partial DB refresh for active site")
    print_at (11,0,"["+fg.yellow+"67 "+fg.white+"] Run Achievement refresh for recent players")
    print_at (12,0,"["+fg.yellow+"666"+fg.white+"] Run complete DB refresh for all players")
    print_at (12,0,"["+fg.yellow+"667"+fg.white+"] Find new players for active site")

    print (" ")
    print ("[x] Exit")
    
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

    print ("%s/***** Select Option ************************************************\%s" % (fg.yellow, fg.white))
    print (preS)
def drawArenaMenu():
    global config
    counter = 5
    print_at (5,0,"%s/***** Pick arena ***************************************************\ %s" % (fg.yellow, fg.white))
    for arena in config["configs"]:
        counter = counter + 1 
        print_at (counter,0,"[%s%i%s] %s" % (Fore.YELLOW,counter -5 ,Fore.WHITE,arena["SiteNameShort"]))
    counter = counter + 1
    print_at (counter,0,"[%sB%s] Return to main menu" % (Fore.YELLOW, Fore.WHITE))
    


def drawOutputPane():
    counter = 0
    print_at (5,0,"%s/***** Output ******************************************************\%s" % (fg.yellow, fg.white))
    for var in feedback[-15:]:
        var = var + " " * 70 
        var = var[0:70] 
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
    

os.system('CLS')
waitingFunction = ""
while inputS != "exit" and inputS != "x": 
    
    inputS = ""
    while not feedbackQueue.q.empty():
        feedback.append(feedbackQueue.q.get())
    while not InputReader.q.empty():
        inputS = InputReader.q.get()
        feedback.append(inputS)


        
    
    if not FetchPlayerUpdatesAndNewPlayers.StatusOfFetchPlayer.empty():    
        CurrentWorkerStatus = FetchPlayerUpdatesAndNewPlayers.StatusOfFetchPlayer.get() #fetch the latest update
        FetchPlayerAndGames.StatusOfFetchPlayer.queue.clear() #purge older updates
    if not FetchPlayerAndGames.StatusOfFetchPlayer.empty():
        CurrentWorkerStatus = FetchPlayerAndGames.StatusOfFetchPlayer.get() #fetch the latest update
        FetchPlayerAndGames.StatusOfFetchPlayer.queue.clear() #purge older updates

    #print(CurrentWorkerStatus)
    #currently prioritise minor update over major update
    
    if waitingFunction == "11":
        
        drawHeader()
        drawArenaMenu()
        print("\nEnter option...")
        if inputS != "":
            if inputS == "b":
                waitingFunction = ""
                
            else:
                setActive(int(inputS)-1)
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
        elif inputS == "5":
            waitingFunction = "5"
        elif inputS == "6":
            import runmeWhenever
            feedback.append("Blobs written")
            
            

        elif inputS == "61":
            
            waitingFunction = "61"
            feedback.append("Enter User ID or GamerTag to search")
        elif inputS == "66":
            feedback.append("Performing partial update in background...")
            t = threading.Thread(target=executeQueryGames, args=("partial",))
            threads.append(t)
            t.start()      
            inputS = ""
        elif inputS == "666":
            feedback.append("Performing complete update in background...")
            t = threading.Thread(target=updateExistingPlayers)
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





