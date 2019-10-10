from console import fg, bg, fx 
from ctypes import *
import os

class COORD(Structure):
    pass
STD_OUTPUT_HANDLE = -11
COORD._fields_ = [("X", c_short), ("Y", c_short)]

def print_at(r, c, s):
    h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    windll.kernel32.SetConsoleCursorPosition(h, COORD(c, r))
    s = s + " "*30
    c = s.encode("windows-1252")
    windll.kernel32.WriteConsoleA(h, c_char_p(c), len(c), None, None)
### END  https://rosettacode.org/wiki/Terminal_control/Cursor_positioning#Python ###

def clearScreen(): 
    os.system('cls')

def endUI():
    clearScreen()