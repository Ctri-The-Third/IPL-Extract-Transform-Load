from console import fg, bg, fx 
import os
import curses
from curses import wrapper
import LinuxInputReader
print("\e[31mRedLinux menus not yet implemented! Please run this application on Windows for now :(\e[39m")

screen = curses.initscr()
curses.start_color()


#PALET
# 0 = White on black
# 1 = Green on Black
# 2 = Yellow on Black
# 3 = Red on Black
# 4 = Black on Green
# 5 = Black on Red
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_RED)



def initUI():
    global screen
    #curses.noecho()
    
    print("INIT")



def print_at(r,c,s,PI = 0):
    if PI > 5 or PI < 0:
        PI = 0


    global screen
    
    screen.addstr(r,c,s,curses.color_pair(PI))
    
    screen.refresh()
    

def clearScreen():
    os.system('clear')

def endUI():
    curses.endwin() 

def startInputThread():
    thread = threading.Thread(target=WinInputReader.executeKeyboardLoop)
    return thread
    