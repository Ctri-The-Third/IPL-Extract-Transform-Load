import os

if os.name == "nt":
    from WinCmdMenus import * 
elif os.name == "posix":
    from LinuxCmdMenus import *
    