import os
import time
import colorama
import threading
import queue 
from console import fg, bg, fx
import console.utils
import console.screen as screen

from renderProgressBar import renderBar
from colorama import Fore
from colorama import Back
from ConfigHelper import getConfig 
from ConfigHelper import setActive
from ConfigHelper import setNewDates

from FetchIndividual import fetchIndividual
from FetchPlayerAndGames import executeQueryGames
import FetchPlayerAndGames

import InputReader


# This application class serves as a wrapper for the initialization of curses
# and also manages the actual forms of the application

feedback = []
threads = []
def drawDateMenu():
    
    config = getConfig()
    print ("%s ***** LF Profiler      ***** %s" % (fg.yellow, fg.white))

    print ("Start Date:          [ %s%s%s ]          |" % ( fg.green,  config["StartDate"], fg.white))
    print ("End Date:            [ %s%s%s ]          |" % ( fg.green, config["EndDate"],fg.white))
    print ("Target site:         [ %s%s%s ]|" % (fg.green,config["SiteNameShort"][0:20],fg.white))
    print ("")

    print ("%s ***** Start Date       ***** %s" % (fg.yellow, fg.white))
    print ("%s In the form YYYY-MM-DD       %s" % (fg.yellow, fg.white))
    print ("%s or 'x' to go back            %s" % (fg.yellow, fg.white))
    return input()
def drawMainMenu():
    time.sleep(0.05)
    emptyString = "                           "
    inputS = ""
    
    config = getConfig()
    
    

    print ("%s ***** LF Profiler      ***** %s" % (fg.yellow, fg.white))

    outStr  = "Start Date:          [ %s%s%s ]          | " % ( fg.green,  config["StartDate"], fg.white)
    outStr = outStr + renderBar((CurrentWorkerStatus["CurEntry"]/CurrentWorkerStatus["TotalEntries"]),fg.black,bg.green)
    outStr = outStr + "\nEnd Date:            [ %s%s%s ]          | " % ( fg.green, config["EndDate"],fg.white)
    outStr = outStr + CurrentWorkerStatus["CurrentAction"]
    outStr = outStr + "\nTarget site:         [ %s%s%s ]| " % (fg.green,config["SiteNameShort"][0:20],fg.white)
    print(outStr)
    print ("")

    print ("%s ***** Menu             ***** %s" % (fg.yellow, fg.white))
    print ("["+fg.yellow+"110"+fg.white+"] Select site - Edinburgh")
    print ("["+fg.yellow+"111"+fg.white+"] Select site - Peterborugh")
    print ("["+fg.yellow+"12 "+fg.white+"] Select different dates")
    print ("["+fg.yellow+" 5 "+fg.white+"] Run queries on specific player")
    print ("["+fg.yellow+" 6 "+fg.white+"] Rebuild the JSON blobs")
    print ("["+fg.yellow+"61 "+fg.white+"] Update individual player")
    print ("["+fg.yellow+"66 "+fg.white+"] Run partial DB refresh")
    print ("["+fg.yellow+"666"+fg.white+"] Run complete DB refresh")

    print (" ")
    print ("[x] Exit")
    
    if feedback.__len__() > 5:
        print ("%s ***** Previous commands ***** %s" % (fg.yellow, fg.white))
        for var in feedback[-5:]:
            print("%s%s%s%s%s" % (bg.green,fg.black,var,bg.black, fg.white))

        
    elif feedback.__len__() != 0:
        print ("%s ***** Previous commands ***** %s" % (fg.yellow, fg.white))
        for var in feedback:
            print("%s%s%s%s%s" % (bg.green,fg.black,var,bg.black, fg.white))

    print ("%s ***** Select Option    ***** %s" % (fg.yellow, fg.white))
    print (preS)
    


preS = ""
inputS = ""

t = threading.Thread(target=InputReader.executeKeyboardLoop)
threads.append(t)
t.start()    
    

console.utils.clear(3)
while inputS != "exit" and inputS != "x": 
    console.utils.clear(1)
    inputS = ""
    while not InputReader.q.empty():
        inputS = InputReader.q.get()
        feedback.append(inputS)
        if inputS == "x":
            True == True 
    

        
    FetchPlayerAndGames.StatusOfFetchPlayer 
    if not FetchPlayerAndGames.StatusOfFetchPlayer.empty():
        CurrentWorkerStatus = FetchPlayerAndGames.StatusOfFetchPlayer.get() #fetch the latest update
        FetchPlayerAndGames.StatusOfFetchPlayer.queue.clear() #purge older updates
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
    elif inputS == "61":
        input() #clear the input
        fetchIndividual()
        
        input ("Press any key to continue...")
    elif inputS == "66":
        feedback.append("Performing partial update in background...")
        t = threading.Thread(target=executeQueryGames, args=("partial",))
        threads.append(t)
        t.start()      
        
        feedback.append("Completed partial update.")
        inputS = ""
    elif inputS == "666":
        feedback.append("Completed full update.")
        import runmeMonthly
        input ("Press any key to continue...")
    time.sleep(2.5)





