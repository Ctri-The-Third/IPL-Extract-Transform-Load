import InputReader
import time
import queue
 
def executeKeyboardLoop():
    
    inputS = ""
    while inputS != "x":
        inputS = input()
        InputReader.q.put(inputS)

