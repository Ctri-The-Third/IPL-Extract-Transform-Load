import requests
import json
import importlib
import datetime

from FetchHelper import fetchPlayer_root
from FetchHelper import fetchPlayerAcheivement_root
from SQLHelper import addAchievement
from SQLHelper import addPlayerAchievement
from SQLHelper import addPlayerAchievementScore


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

    for centre in allAchievements["centre"]:
        if centre["name"] == "Funstation Ltd, Edinburgh, Scotland":


            addPlayerAchievementScore(ID,centre["score"])
            #print (allAchievements)
            for achievement in centre["achievements"]:
                addAchievement(achievement["name"],achievement["description"],achievement["image"])
                addPlayerAchievement(achievement["image"],ID,achievement["newAchievement"],achievement["achievedDate"],achievement["progressA"],achievement["progressB"])
                