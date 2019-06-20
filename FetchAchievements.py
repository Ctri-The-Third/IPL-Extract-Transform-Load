import requests
import json
import importlib
import datetime

from FetchHelper import fetchPlayer_root
from FetchHelper import fetchPlayerAcheivement_root
from SQLHelper import addAchievement
from SQLHelper import addPlayerAchievement


targetIDs = {
'7-9-8167',	#Billybob
'9-6-106',	#C'tri
'7-9-1996',	#Paradigm
'7-9-13958',	#Robo_h34d
'7-9-2331',	#Reboot
'7-9-13899',	#Thorian
}

for ID in targetIDs:
    IDpieces = ID.split("-")
    allAchievements = fetchPlayerAcheivement_root('',IDpieces[0],IDpieces[1],IDpieces[2])