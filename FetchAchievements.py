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
from SQLHelper import getPlayersWhoMightNeedAchievementUpdates
from ConfigHelper import getConfig

#config = getConfig()
#targetIDs = getInterestingPlayersRoster(False,config['EndDate'],config['ChurnDuration'])
#targetIDs = {
#    '7-9-5940'
#}
def executeFetchAchievements (scope):
    config = getConfig()
    if scope == "full":
        targetIDs = getInterestingPlayersRoster(True,config['StartDate'],config['ChurnDuration'])
    else:
        targetIDs = getPlayersWhoMightNeedAchievementUpdates(scope)
    
    print("Scope : %s" % (scope))
    fetchAllAchievements(targetIDs)

def fetchAllAchievements (targetIDs):
    config = getConfig()
    totalToUpdate = len(targetIDs)
    startTime = datetime.datetime.now()
    playerCounter = 0
    for ID in targetIDs:
        playerCounter = playerCounter + 1
        IDpieces = ID.split("-")
        allAchievements = fetchPlayerAcheivement_root('',IDpieces[0],IDpieces[1],IDpieces[2])
        if allAchievements.__len__() > 0:
            for centre in allAchievements["centre"]:
                if centre["name"] == config["SiteNameReal"]:


                    addPlayerAchievementScore(ID,centre["score"])
                    #print (allAchievements)
                    for achievement in centre["achievements"]:
                        addAchievement(achievement["name"],achievement["description"],achievement["image"], config["SiteNameReal"])
                        addPlayerAchievement(achievement["image"],ID,achievement["newAchievement"],achievement["achievedDate"],achievement["progressA"],achievement["progressB"])
                totalAchievemnts = len(centre["achievements"])
            print ("Updated %i achievements for player %s. [%i/%i]" % (totalAchievemnts,ID,playerCounter,totalToUpdate))
    endTime = datetime.datetime.now()
    f = open("Stats.txt","a+")
    f.write("Queried {0} players' achievements, operation completed after {1}. \t\n".format(len(targetIDs),endTime - startTime ))
    f.close()

def manualTargetAchievements(targetID):
    fetchAllAchievements([targetID])

