import os
import colorama
from colorama import Fore
from ConfigHelper import getConfig 
# This application class serves as a wrapper for the initialization of curses
# and also manages the actual forms of the application

inputS = ""
feedbackS = ""
config = getConfig()
while inputS != "x":
    os.system('cls')

    print ("%s ***** LF Profiler      ***** %s" % (Fore.YELLOW, Fore.WHITE))

    print ("Start Date:          [ %s%s%s ]" % ( Fore.GREEN,config["StartDate"], Fore.WHITE))
    print ("End Date:            [ %s%s%s ]" % ( Fore.GREEN,config["EndDate"],Fore.WHITE))
    print ("Target site:         [ %s%s%s ]" % (Fore.GREEN,config["SiteNameShort"],Fore.WHITE))
    print ("")

    print ("%s ***** Menu             ***** %s" % (Fore.YELLOW, Fore.WHITE))
    print ("["+Fore.YELLOW+"11"+Fore.WHITE+"] Select different site")
    print ("["+Fore.YELLOW+"12"+Fore.WHITE+"] Select different dates")
    print ("["+Fore.YELLOW+" 5"+Fore.WHITE+"] Run queries on specific player")
    print ("["+Fore.YELLOW+" 6"+Fore.WHITE+"] Rebuild the JSON blobs")
    print ("["+Fore.YELLOW+"61"+Fore.WHITE+"] Update individual player")
    print ("["+Fore.YELLOW+"66"+Fore.WHITE+"] Run partial DB refresh")
    print ("["+Fore.YELLOW+"666"+Fore.WHITE+"] Run complete DB refresh")

    print (" ")
    print ("[x] Exit")
    
    if inputS != "":
        print ("%s ***** Previous command ***** %s" % (Fore.YELLOW, Fore.WHITE))
        print ("%s %s %s" % (Fore.GREEN, inputS, Fore.WHITE))
        print ("%s %s %s" % (Fore.GREEN, feedbackS, Fore.WHITE))
    print ("%s ***** Select Option    ***** %s" % (Fore.YELLOW, Fore.WHITE))
    
    inputS = input()
    feedbackS = ""
    if inputS == "1":
        feedbackS = feedbackS + "\n not yet implemented"
    elif inputS == "5":
        feedbackS = feedbackS + "\n not yet implemented"
    elif inputS == "6":
        import runmeWhenever
    elif inputS == "61":
        import ExecuteFetchIndividual
    elif inputS == "66":
        import runmeWeekly
    elif inputS == "666":
        import runmeMonthly
