import os
import colorama
from colorama import Fore
from colorama import Back
from ConfigHelper import getConfig 
from ConfigHelper import setActive
# This application class serves as a wrapper for the initialization of curses
# and also manages the actual forms of the application

feedback = []


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
        feedback.append("not yet implemented")
    elif inputS == "5":
        feedback.append("not yet implemented")
    elif inputS == "6":
        import runmeWhenever
        feedback.append("Blobs written")
    elif inputS == "61":
        import ExecuteFetchIndividual
    elif inputS == "66":
        feedback.append("Performing partial update...")
        import runmeWeekly
        feedback.append("Completed partial update.")
    elif inputS == "666":
        import runmeMonthly
