import os
import time
import math


if os.name == "nt":
    from WinCmdMenus import * 
elif os.name == "posix":
    from LinuxCmdMenus import *
    

def renderBar(progress,row,colum,firstColourPairIndex,secondColourPairIndex):
    returnString = ""
    #print_at(1,0,"[%s,%s]"%(row,colum),5)
    progress = round(progress * 10000) / 100
    returnString = "%g%%" % progress
    lpadding = math.ceil(10-len(returnString)/2)
    rpadding = math.floor(10-len(returnString)/2)
    
    lstring = " " * lpadding
    rstring = " " * rpadding

    returnString = "%s%s%s" % (lstring,returnString,rstring)
    progressi = math.floor(progress /5 )
    
    print_at(row,colum,"[",PI =1)
    print_at(row,colum+1,returnString[0:progressi],firstColourPairIndex)
    
    print_at(row,(colum+progressi+1),returnString[progressi:len(returnString)],secondColourPairIndex)
    print_at(row,(colum+21),"]",PI =1) 

    return returnString

#for i in range (49):
    #i = i + 1
    #print(renderBar(i/50,colorama.Fore.BLACK, colorama.Back.GREEN))
    #time.sleep (0.1)
    
