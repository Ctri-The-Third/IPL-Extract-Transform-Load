from console import fg, bg, fx 
import os
import curses
from curses import wrapper
import LinuxInputReader
import threading
import InputReader
import pynput
from pynput.keyboard import Key, Controller
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
    curses.start_color()
    screen = curses.initscr()
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
    screen.addstr(r,c,s,curses.color_pair(PI))
    
def clearScreen():
    os.system('clear')

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
    global inputString

    
    text = ""
    while text != "x":
        win = curses.newwin(26,0,20,30)
        tb = curses.textpad.Textbox(win)
        text = tb.edit(__enter_is_terminate__)[:-2].rstrip()
        InputReader.q.put(text)
        del win 

def __enter_is_terminate__(x):
    if x == 10:
        return 7
    else:
        return x
