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
import ConfigHelper as cfg

#config = getConfig()
#targetIDs = getInterestingPlayersRoster(False,cfg.getConfigString("EndDate'],cfg.getConfigString("ChurnDuration'])
#targetIDs = {
#    '7-9-5940'
#}
def executeFetchAchievements (scope):
    
    if scope == "full":
        targetIDs = getInterestingPlayersRoster(True,cfg.getConfigString("StartDate"),cfg.getConfigString("ChurnDuration"))
    else:
        targetIDs = getPlayersWhoMightNeedAchievementUpdates(scope)
    
    print("Scope : %s" % (scope))
    fetchAllAchievements(targetIDs)

def fetchAllAchievements (targetIDs):
    
    totalToUpdate = len(targetIDs)
    startTime = datetime.datetime.now()
    playerCounter = 0
    for ID in targetIDs:
        playerCounter = playerCounter + 1
        IDpieces = ID.split("-")
        
        allAchievements = fetchPlayerAcheivement_root('',IDpieces[0],IDpieces[1],IDpieces[2])
        
        totalAchievemnts = 0
        
        if allAchievements.__len__() > 0:
            if '1' in allAchievements["centre"]:
                print("DBG: FetchAchievements.fetchAllAchivements: ABNORMAL RESPONSE handled for user %s" % (ID) )
                print("DBG: FetchAchievements.fetchAllAchivements: Manually check they don't have multiple sites' achievements" )
                holdingVar = []
                holdingVar.append( allAchievements["centre"]['1'])
                allAchievements["centre"] = holdingVar
                #print (json.dumps(allAchievements["centre"]))
            for centre in allAchievements["centre"]:
                if centre["name"] == cfg.getConfigString("SiteNameReal"): #Since we have to do small updates of every arena anyway, it's only when we have recent crossplaying that we have to worry about pinging IPL multiple times per user.


                    addPlayerAchievementScore(ID,centre["score"])
                    #print (allAchievements)
                    for achievement in centre["achievements"]:
                        uuid = addAchievement(achievement["name"],achievement["description"],achievement["image"], cfg.getConfigString("SiteNameReal"))
                        addPlayerAchievement(uuid,ID,achievement["newAchievement"],achievement["achievedDate"],achievement["progressA"],achievement["progressB"])
                    totalAchievemnts = len(centre["achievements"])
            print ("Updated %i achievements for player %s. [%i/%i]" % (totalAchievemnts,ID,playerCounter,totalToUpdate))
        
    endTime = datetime.datetime.now()
    f = open("Stats.txt","a+")
    f.write("Queried {0} players' achievements, operation completed after {1}. \t\n".format(len(targetIDs),endTime - startTime ))
    f.close()

def manualTargetAchievements(targetID):
    fetchAllAchievements([targetID])


#manualTargetAchievements ("9-6-106")
#manualTargetAchievements ("7-2-43548")