from pynput.keyboard import Key, Listener
import time
import pynput
import queue
 
q = queue.Queue()
def executeKeyboardLoop():
    global q 
    inputS = ""
    while inputS != "x":
        inputS = input()
        q.put(inputS)

