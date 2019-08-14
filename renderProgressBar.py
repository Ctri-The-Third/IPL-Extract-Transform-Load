import os
import colorama
import time
import math
def renderBar(progress,forecolor,backcolor):
    returnString = ""
    
    progress = round(progress * 10000) / 100
    returnString = "%g%%" % progress
    lpadding = math.ceil(10-len(returnString)/2)
    rpadding = math.floor(10-len(returnString)/2)
    
    lstring = " " * lpadding
    rstring = " " * rpadding

    returnString = "%s%s%s" % (lstring,returnString,rstring)
    progressi = math.floor(progress /10 )
    returnString = "[%s%s"%(forecolor,backcolor)+returnString[0:progressi]+"%s%s"% (colorama.Fore.WHITE,colorama.Back.BLACK)+ returnString[progressi:len(returnString)]+"%s%s]" % (colorama.Fore.WHITE,colorama.Back.BLACK)
    print(progressi)
    
    return returnString

