import queue
import curses
import os
from DBG import * 
import time
import InputReader
q = queue.Queue()
_started = False
_screen = None

def start():    
    global _started 
    global _screen
    
    _started = True
    _screen = curses.initscr()
    curses.start_color()
    curses.noecho()
    curses.cbreak()
    
    _screen.nodelay(True)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_RED)

    execute()
    _end()


def end():
    global _started
    _started = False


def execute():
    global _started
    inputString = ''
    while _started:
        # RENDER INSTRUCTIONS IN
        while q.empty() == False: 
            printObj = q.get()
            try:
                if printObj["instr"] == "clr":
                    _clearScreen()
                elif printObj["instr"] == "print":
                    _print_at(printObj["r"],printObj["c"],printObj["s"],printObj["PI"])
                    pass    
            except Exception as e:
                DBG("LinuxRenderThread.execute - error in parsing q object: %s" % (e,),3)
        
            # KEY INSTRUCTIONS OUT 
            try:
                key = _screen.getkey()

                if str(key) == '^?' or key == '\x7f':
                    inputString = inputString[:-1]
                elif str(key) == '\n':
                    InputReader.q.put(inputString)
                    inputString = ''
                else:
                    inputString += str(key)
                
            except Exception as e: 
                pass
            
        _drawScreen()
        time.sleep(0.015)
    _end()


def _print_at(r,c,s,PI = 0):
    global _screen
    if _screen == None:
        print ("Have you run initUI yet?")
        return
    if PI > 5 or PI < 0:
        PI = 0
    try:
        _screen.addstr(r,c,s,curses.color_pair(PI))
    except:
        pass
    
    
def _clearScreen():
    global _screen
    os.system('clear')
    _screen.redrawwin()


 
def _end():
    global _started
    global _screen
    curses.endwin() 
    _screen.nodelay(False)
    curses.echo()
    curses.nocbreak()



def _printat():
    return

def _drawScreen():
    
    global _screen
    _screen.refresh()