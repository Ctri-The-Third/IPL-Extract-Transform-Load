from console import fg, bg, fx 
from ctypes import *

import threading
import os
import InputReader
import time
import queue

#PALET
# 0 = white on black
# 1 = green on black
# 2 = Yellow on black
# 3 = red on black
# 4 = black on green
# 5 = black on red

colourPairs = [
    "%s%s"% (fg.white,bg.black),
    "%s%s"% (fg.green,bg.black),
    "%s%s"% (fg.yellow, bg.black),
    "%s%s"% (fg.red,bg.black),
    "%s%s"% (fg.black,bg.green),
    "%s%s"% (fg.black,bg.red)
]
def initUI():
    return 

class COORD(Structure):
    pass
STD_OUTPUT_HANDLE = -11
COORD._fields_ = [("X", c_short), ("Y", c_short)]



def print_at(r, c, s, PI=0):
    if PI > 5 or PI < 0:
        PI = 0
    
    h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    windll.kernel32.SetConsoleCursorPosition(h, COORD(c, r))
    s = "%s%s%s" %(colourPairs[PI],s,colourPairs[PI])
    c = s.encode("windows-1252")
    windll.kernel32.WriteConsoleA(h, c_char_p(c), len(c), None, None)
### END  https://rosettacode.org/wiki/Terminal_control/Cursor_positioning#Python ###

def clearScreen(): 
    print_at(0,0," clearing string ",0)
    os.system('cls')

def endUI():
    clearScreen()

def startInputThread():
    thread = threading.Thread(target=__inputThread__)
    thread.start()
    return thread

def drawScreen():
    return 
 
def __inputThread__():
    
    inputS = ""
    while inputS != "x":
        inputS = input()
        InputReader.q.put(inputS)
