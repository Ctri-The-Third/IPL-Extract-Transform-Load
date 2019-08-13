import os
import colorama
import threading
from colorama import Fore
from colorama import Back
from ConfigHelper import getConfig 
from ConfigHelper import setActive
from ConfigHelper import setNewDates

from FetchPlayerAndGames import executeQueryGames

# This application class serves as a wrapper for the initialization of curses
# and also manages the actual forms of the application

feedback = []
threads = []
def drawDateMenu():
    os.system('cls')
    config = getConfig()
    print ("%s ***** LF Profiler      ***** %s" % (Fore.YELLOW, Fore.WHITE))

    print ("Start Date:          [ %s%s%s ]          |" % ( Fore.GREEN,  config["StartDate"], Fore.WHITE))
    print ("End Date:            [ %s%s%s ]          |" % ( Fore.GREEN, config["EndDate"],Fore.WHITE))
    print ("Target site:         [ %s%s%s ]|" % (Fore.GREEN,config["SiteNameShort"][0:20],Fore.WHITE))
    print ("")

    print ("%s ***** Start Date       ***** %s" % (Fore.YELLOW, Fore.WHITE))
    print ("%s In the form YYYY-MM-DD       %s" % (Fore.YELLOW, Fore.WHITE))
    print ("%s or 'x' to go back            %s" % (Fore.YELLOW, Fore.WHITE))
    return input()
def drawMainMenu():
    emptyString = "                           "
    inputS = ""
    
    config = getConfig()
    
    os.system('cls')

    print ("%s ***** LF Profiler      ***** %s" % (Fore.YELLOW, Fore.WHITE))

    print ("Start Date:          [ %s%s%s ]          |" % ( Fore.GREEN,  config["StartDate"], Fore.WHITE))
    print ("End Date:            [ %s%s%s ]          |" % ( Fore.GREEN, config["EndDate"],Fore.WHITE))
    print ("Target site:         [ %s%s%s ]|" % (Fore.GREEN,config["SiteNameShort"][0:20],Fore.WHITE))
    print ("")

    print ("%s ***** Menu             ***** %s" % (Fore.YELLOW, Fore.WHITE))
    print ("["+Fore.YELLOW+"110"+Fore.WHITE+"] Select site - Edinburgh")
    print ("["+Fore.YELLOW+"111"+Fore.WHITE+"] Select site - Peterborugh")
    print ("["+Fore.YELLOW+"12 "+Fore.WHITE+"] Select different dates")
    print ("["+Fore.YELLOW+" 5 "+Fore.WHITE+"] Run queries on specific player")
    print ("["+Fore.YELLOW+" 6 "+Fore.WHITE+"] Rebuild the JSON blobs")
    print ("["+Fore.YELLOW+"61 "+Fore.WHITE+"] Update individual player")
    print ("["+Fore.YELLOW+"66 "+Fore.WHITE+"] Run partial DB refresh")
    print ("["+Fore.YELLOW+"666"+Fore.WHITE+"] Run complete DB refresh")

    print (" ")
    print ("[x] Exit")
    
    if feedback.__len__() != 0:
        print ("%s ***** Previous commands ***** %s" % (Fore.YELLOW, Fore.WHITE))
        for var in feedback:
            print("%s%s%s%s%s" % (Back.GREEN,Fore.BLACK,var,Back.BLACK, Fore.WHITE))

    print ("%s ***** Select Option    ***** %s" % (Fore.YELLOW, Fore.WHITE))
    
    return input()
        
    

inputS = ""

while inputS != "x":
    inputS = drawMainMenu()
    feedback.append(inputS)
    
    if inputS == "110":
        feedback.append(setActive(0))
    if inputS == "111":
        feedback.append(setActive(1))
    if inputS == "12":
        
        startDate = drawDateMenu()
        print ("%s ***** End Date         ***** %s" % (Fore.YELLOW, Fore.WHITE))
        EndDate = input()

        if startDate != "x" and EndDate != "x":
            feedback.append(setNewDates(startDate,EndDate))
        
    elif inputS == "5":
        feedback.append("not yet implemented")
    elif inputS == "6":
        import runmeWhenever
        feedback.append("Blobs written")
    elif inputS == "61":
        
        import ExecuteFetchIndividual
        
        input ("Press any key to continue...")
    elif inputS == "66":
        feedback.append("Performing partial update in background...")
        t = threading.Thread(target=executeQueryGames, args=("partial",))
        
        threads.append(t)
        t.start()      
        
        feedback.append("Completed partial update.")
    elif inputS == "666":
        feedback.append("Completed full update.")
        import runmeMonthly
        input ("Press any key to continue...")



GuiQueue.put()

