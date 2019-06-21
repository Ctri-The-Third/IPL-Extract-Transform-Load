import requests
import json
import importlib
import datetime

from FetchHelper import fetchPlayer_root
from FetchHelper import fetchPlayerAcheivement_root
from SQLHelper import addAchievement
from SQLHelper import addPlayerAchievement
from SQLHelper import addPlayerAchievementScore
from SQLHelper import getInterestingPlayersRoster


targetIDs = getInterestingPlayersRoster()
startTime = datetime.datetime.now()
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
endTime = datetime.datetime.now()
f = open("Stats.txt","a+")
f.write("Queried {0} players' achievements, operation completed after {1}. \t\n".format(len(targetIDs),endTime - startTime ))
f.close()