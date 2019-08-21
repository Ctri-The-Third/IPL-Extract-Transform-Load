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
from FetchIndividual import fetchIndividual
from FetchPlayerAndGames import executeQueryGames
from FetchPlayerUpdatesAndNewPlayers import updateExistingPlayers
import FetchPlayerAndGames
import FetchPlayerUpdatesAndNewPlayers

import InputReader


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
 
    c = s.encode("windows-1252")
    windll.kernel32.WriteConsoleA(h, c_char_p(c), len(c), None, None)
### END  https://rosettacode.org/wiki/Terminal_control/Cursor_positioning#Python ###


def drawDateMenu():
    os.system('CLS')
    config = getConfig()
    print_at (0,0,"%s/***** LF Profiler **************************************************\ %s" % (fg.yellow, fg.white))

    print_at (1,0, "Start Date:          [ %s%s%s ]          |" % ( fg.green,  config["StartDate"], fg.white))
    print_at (2,0,"End Date:            [ %s%s%s ]          |" % ( fg.green, config["EndDate"],fg.white))
    print_at (3,0,"Target site:         [ %s%s%s ]|" % (fg.green,config["SiteNameShort"][0:20],fg.white))
    

    print_at (4,0, "%s/***** Start Date ***************************************************\%s" % (fg.yellow, fg.white))
    print_at (5,0,"%s In the form YYYY-MM-DD       %s" % (fg.yellow, fg.white))
    print_at (6,0,"%s or 'x' to go back            %s" % (fg.yellow, fg.white))
    print_at (7,0,"")
    return input("Enter Start Date: ")
def drawMainMenu():
    #time.sleep(0.05)
    emptyString = "                           "
    inputS = ""
    
    config = getConfig()

    print_at (0,0,"%s/***** LF Profiler **************************************************\ %s" % (fg.yellow, fg.white))

    outStr  = "Start Date:           [ %s%s%s ]          | " % ( fg.green,  config["StartDate"], fg.white)
    outStr = outStr + renderBar((CurrentWorkerStatus["CurEntry"]/CurrentWorkerStatus["TotalEntries"]),fg.black,bg.green)
    outStr = outStr + "\nEnd Date:             [ %s%s%s ]          | " % ( fg.green, config["EndDate"],fg.white)
    outStr = outStr + CurrentWorkerStatus["CurrentAction"]
    outStr = outStr + "\nTarget site:          [ %s%s%s ]| " % (fg.green,config["SiteNameShort"][0:20],fg.white) 
    outStr = outStr + "%s" % (CurrentWorkerStatus["ETA"]) 
    print_at (1,0,outStr)
    print_at (4,0,"")

    print_at (5,0,"%s/***** Menu *********************************************************\ %s" % (fg.yellow, fg.white))
    print_at (6,0,"["+fg.yellow+"110"+fg.white+"] Select site - Edinburgh")
    print_at (7,0,"["+fg.yellow+"111"+fg.white+"] Select site - Peterborugh")
    print_at (8,0,"["+fg.yellow+"12 "+fg.white+"] Select different dates")
    print_at (9,0,"["+fg.yellow+" 5 "+fg.white+"] Run queries on specific player")
    print_at (10,0,"["+fg.yellow+" 6 "+fg.white+"] Rebuild the JSON blobs")
    print_at (11,0,"["+fg.yellow+"61 "+fg.white+"] Update individual player")
    print_at (12,0,"["+fg.yellow+"66 "+fg.white+"] Run partial DB refresh")
    print_at (13,0,"["+fg.yellow+"666"+fg.white+"] Run complete DB refresh")

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
    


preS = ""
inputS = ""

t = threading.Thread(target=InputReader.executeKeyboardLoop)
threads.append(t)
t.start()    
    

os.system('CLS')
while inputS != "exit" and inputS != "x": 
    
    inputS = ""
    while not InputReader.q.empty():
        inputS = InputReader.q.get()
        feedback.append(inputS)
        if inputS == "x":
            True == True 
    

        
    
    if not FetchPlayerUpdatesAndNewPlayers.StatusOfFetchPlayer.empty():    
        CurrentWorkerStatus = FetchPlayerUpdatesAndNewPlayers.StatusOfFetchPlayer.get() #fetch the latest update
        FetchPlayerAndGames.StatusOfFetchPlayer.queue.clear() #purge older updates
    if not FetchPlayerAndGames.StatusOfFetchPlayer.empty():
        CurrentWorkerStatus = FetchPlayerAndGames.StatusOfFetchPlayer.get() #fetch the latest update
        FetchPlayerAndGames.StatusOfFetchPlayer.queue.clear() #purge older updates

    #print(CurrentWorkerStatus)
    #currently prioritise minor update over major update
    drawMainMenu()
    

    
    
    
    if inputS == "110":
        feedback.append(setActive(0))
    if inputS == "111":
        feedback.append(setActive(1))
    if inputS == "12":
        startDate = drawDateMenu()
        print ("%s ***** End Date         ***** %s" % (fg.yellow, fg.white))
        EndDate = input()

        if startDate != "x" and EndDate != "x":
            feedback.append(setNewDates(startDate,EndDate))
    elif inputS == "5":
        feedback.append("not yet implemented")
    elif inputS == "6":
        import runmeWhenever
        feedback.append("Blobs written")
        input ("Press any key to continue...")
        os.system('CLS')

    elif inputS == "61":
        input() #clear the input
        fetchIndividual()
        
        input ("Press any key to continue...")
        os.system('CLS')
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
    time.sleep(.5)





