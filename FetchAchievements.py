import math 
import time
from DBG import DBG 
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
import workerProgressQueue as wpq
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
    totalPlayerCount = len(targetIDs)
    for ID in targetIDs:

        ETA = "Calculating"
        if playerCounter >= 5:
            delta = ((datetime.datetime.now() - startTime).total_seconds() / playerCounter) 
            delta = (totalPlayerCount - playerCounter) * delta #seconds remaining
            seconds = round(delta,0)
            minutes = 0
            hours = 0

            if (seconds > 60 ):
                minutes = math.floor(seconds / 60)
                seconds = seconds % 60 
            if (minutes > 60):
                hours = math.floor(minutes / 60 )
                minutes = minutes % 60
            
            delta = "%ih, %im, %is" % (hours,minutes,seconds)
            ETA = delta
            
            
        else:
            ETA = "Calculating"

        playerCounter = playerCounter + 1
        IDpieces = ID.split("-")
        
        region = IDpieces[0]
        site =  IDpieces[1]
        IDPart = IDpieces[2]
        
        DBGstring = "Seeking Achs for %s-%s-%s, [%i / %i] : " % (region,site,IDPart,playerCounter,totalPlayerCount)
        wpq.updateQ(playerCounter,totalPlayerCount, "Achs for %s-%s-%s" % (region,site,IDPart),ETA)
    
        allAchievements = fetchPlayerAcheivement_root('',IDpieces[0],IDpieces[1],IDpieces[2])
        
        totalAchievemnts = 0
        
        if allAchievements.__len__() > 0:
            if '1' in allAchievements["centre"]:
                DBG("DBG: FetchAchievements.fetchAllAchivements: ABNORMAL RESPONSE handled for user %s" % (ID) ,2)
                DBG("DBG: FetchAchievements.fetchAllAchivements: Manually check they don't have multiple sites' achievements" ,2)
                holdingVar = []
                holdingVar.append( allAchievements["centre"]['1'])
                allAchievements["centre"] = holdingVar
                #print (json.dumps(allAchievements["centre"]))
            for centre in allAchievements["centre"]:
                #we don't filter by arena, becuase we do achievement searches seperately, and because IPL has to do all the hard work each request anyway.
                #this means less requests against IPL if we do achieves globally.


                #addPlayerAchievementScore(ID,centre["score"])
                #print (allAchievements)
                for achievement in centre["achievements"]:
                    uuid = addAchievement(achievement["name"],achievement["description"],achievement["image"], centre['name'])
                    addPlayerAchievement(uuid,ID,achievement["newAchievement"],achievement["achievedDate"],achievement["progressA"],achievement["progressB"])
                totalAchievemnts = totalAchievemnts + len(centre["achievements"])
            print ("Updated %i achievements for player %s. [%i/%i]" % (totalAchievemnts,ID,playerCounter,totalToUpdate))
        
    endTime = datetime.datetime.now()
    f = open("Stats.txt","a+")
    f.write("Queried {0} players' achievements, operation completed after {1}. \t\n".format(len(targetIDs),endTime - startTime ))
    f.close()

def manualTargetAchievements(targetID):
    fetchAllAchievements([targetID])


#manualTargetAchievements ("9-6-106")
#manualTargetAchievements ("7-2-43548")