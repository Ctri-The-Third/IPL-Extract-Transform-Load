import InputReader
import curses 
from curses.textpad import Textbox, rectangle

def executeKeyboardLoop():
    
    inputS = ""
    while inputS != "x":
        inputS = input()
        InputReader.q.put(inputS)

stdscr = curses.initscr()
curses.nocbreak()
stdscr.keypad(True)
message = ""
while True:
    
    #stdscr.addstr(0, 0, "Enter IM message: (hit Ctrl-G to send)")
    stdscr.addstr(4 ,0,"Enter message! %s" % message)
    rectangle(stdscr, 1,0, 1+1+1, 1+30+1)
    stdscr.refresh()    
    message = stdscr.getstr(2,1,30)
    message = message.decode("utf-8")
    if message == "x":
        break
    # Get resulting contents
    
    

curses.echo()
stdscr.keypad(False)
curses.endwin()