import os
import curses
from curses import wrapper

import threading
import InputReader
import LinuxRenderThread as LRT
print("\e[31mRedLinux menus not yet implemented! Please run this application on Windows for now :(\e[39m")

screen = None  


#PALET
# 0 = White on black
# 1 = Green on Black
# 2 = Yellow on Black
# 3 = Red on Black
# 4 = Black on Green
# 5 = Black on Red

inputString = ""


def initUI():
    t = threading.Thread(target=LRT.start)
    t.start()
    return t 
    
    #

def print_at(r,c,s,PI = 0):
    obj = {"instr":"print","r":r,"c":c,"s":s,"PI":PI}
    LRT.q.put(obj)
    
    
def clearScreen():
    data = {"instr":"clear"}
    LRT.q.put(data)

def drawScreen():
    return #happens automatically 

def endUI():
    print ("Exited menus")
    LRT.end()

def startInputThread():
    # included within render thread
    return

