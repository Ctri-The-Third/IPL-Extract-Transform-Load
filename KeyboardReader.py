from pynput.keyboard import Key, Listener
import time
import pynput
import queue

sentence = ""
 
def keyPress(key):
    q.put(str(key))
    if key == Key.esc:
        # Stop listener
        return False

listener = pynput.keyboard.Listener(
    on_release=keyPress
)
q = queue.Queue()
listener.start()

def convertKey(sentence, key):
    
    d = {}
    d["'0'"] = '0'
    d["'1'"] = '1'
    d["'2'"] = '2'
    d["'3'"] = '3'
    d["'4'"] = '4'
    d["'5'"] = '5'
    d["'6'"] = '6'
    d["'7'"] = '7'
    d["'8'"] = '8'
    d["'9'"] = '9'
    d["'-'"] = '-'


    d["'a'"] = 'a'
    d["'b'"] = 'b'
    d["'c'"] = 'c'
    d["'d'"] = 'd'
    d["'e'"] = 'e'
    d["'f'"] = 'f'
    d["'g'"] = 'g'
    d["'h'"] = 'h'
    d["'i'"] = 'i'
    d["'j'"] = 'j'
    d["'k'"] = 'k'
    d["'l'"] = 'l'
    d["'m'"] = 'm'
    d["'n'"] = 'n'
    d["'o'"] = 'o'
    d["'p'"] = 'p'
    d["'q'"] = 'q'
    d["'r'"] = 'r'
    d["'s'"] = 's'
    d["'t'"] = 't'
    d["'u'"] = 'u'
    d["'v'"] = 'v'
    d["'w'"] = 'w'
    d["'x'"] = 'x'
    d["'y'"] = 'y'
    d["'z'"] = 'z'
    d["Key.space"] = ' '
    d["Key.enter"] = '⏎'
    
    if d.__contains__(key):
        sentence = sentence + d[key]
    if key == "Key.backspace" and sentence is not None: 
        sentence = sentence[0:-1]
    return sentence


#
#def __start__():
#    sentence = ""
#    while sentence != "exit⏎": 
#        while not q.empty():
#            sentence = convertKey(sentence,q.get())
#        time.sleep(0.1)

