import os
import curses
from curses import wrapper

import threading
import InputReader
import pynput
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
    global screen
    global keyboard
    #curses.noecho()
    screen = curses.initscr()
    curses.start_color()
    
    curses.noecho()
    curses.cbreak()

    
    screen.nodelay(True)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_RED)

 


def print_at(r,c,s,PI = 0):
    global screen
    if screen == None:
        print ("Have you run initUI yet?")
        return
    if PI > 5 or PI < 0:
        PI = 0
    try:
        screen.addstr(r,c,s,curses.color_pair(PI))
    except Exception as e:
        pass
    
    
def clearScreen():
    global screen
    os.system('clear')
    screen.redrawwin()


def drawScreen():
    global screen
    screen.refresh()

def endUI():
    curses.endwin() 
    screen.nodelay(False)
    curses.echo()
    curses.nocbreak()

    print ("Exited menus")


def startInputThread():
    thread = threading.Thread(target=__inputThread__)
    thread.start()
    return thread

def __inputThread__():
    global screen
    inputString = ''
    while inputString != "x\n":
        try:
            key = screen.getkey()

            if str(key) == '^?' or key == '\x7f':
                inputString = inputString[:-1]
            elif str(key) == '\n':
                InputReader.q.put(inputString)
                inputString = ''
            else:
                inputString += str(key)
            
            #clearScreen()
            #print_at(1,1,inputString)

            
        except Exception as e: 
            #no input
            pass

