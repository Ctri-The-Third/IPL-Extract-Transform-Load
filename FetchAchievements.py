import binascii
import math 
import time
from DBG import DBG 
import requests
import json
import hashlib
import datetime

from FetchHelper import fetchPlayer_root
from FetchHelper import fetchPlayerAcheivement_root
from SQLHelper import addAchievement
from SQLHelper import addPlayerAchievement
from SQLHelper import addPlayerAchievementScore
from SQLHelper import getInterestingPlayersRoster
from SQLHelper import getPlayersWhoMightNeedAchievementUpdates
from SQLHelper import jobStart, jobHeartbeat, jobEnd
from SQLconnector import connectToSource
import workerProgressQueue as wpq
import ConfigHelper as cfg

#config = getConfig()
#targetIDs = getInterestingPlayersRoster(False,cfg.getConfigString("EndDate'],cfg.getConfigString("ChurnDuration'])
#targetIDs = {
#    '7-9-5940'
#}
def executeFetchAchievements (scope, jobID = None, offset = 0):
    params = {}
    params["scope"] = scope
    
    if scope == "full":
        targetIDs = getInterestingPlayersRoster(True,cfg.getConfigString("StartDate"),cfg.getConfigString("ChurnDuration"),offset=offset)
        if jobID == None: 
            jobID=jobStart("Fetch achievements, inactive players",0,"FetchAchievements.executeFetchAchievements",params, len(targetIDs))
    elif scope == "partial":
        targetIDs = getInterestingPlayersRoster(False,cfg.getConfigString("StartDate"),cfg.getConfigString("ChurnDuration"), offset=offset)
        if jobID == None: 
            jobID=jobStart("Fetch achievements, active players",0,"FetchAchievements.executeFetchAchievements",params,len(targetIDs))
    elif scope == "recent":
        targetIDs = getPlayersWhoMightNeedAchievementUpdates(scope, offset=offset)
        if jobID == None: 
            jobID= jobStart("Fetch achievements, players from the last 7 days",0,"FetchAchievements.executeFetchAchievements",params,len(targetIDs))
    
    print("Scope : %s" % (scope))
    fetchAllAchievements(targetIDs, jobID=jobID)

def fetchAllAchievements (targetIDs, jobID = None):
    conn = connectToSource()
    cursor = conn.cursor()
    totalToUpdate = len(targetIDs)
    offset = 0
    
    if jobID == None: 
        jobID = jobStart("Fetch summaries, all known players",0,"FetchPlayerUpdatesAndNewPlayers.updateExistingPlayers",None)
        startTime = datetime.datetime.now()
    else:
        query = """select ID, started,lastheartbeat,resumeindex, methodname from jobslist 
where finished is null and ID = %s and methodname = 'FetchAchievements.executeFetchAchievements'
order by started desc"""
        cursor.execute(query, (jobID,))
        results = cursor.fetchone()
        if results is None:
            DBG("Could not find valid achievement job for ID [%s] , aborting!" % jobID,1)
            return
        if results[2] is not None:
            startTime = results [2]
        else:
            startTime = results[1]
        if results[3] is not None:
            offset = results[3]
        

    playerCounter = offset
    totalPlayerCount = len(targetIDs)
    lastHeartbeat = startTime
    for ID in targetIDs:
        IDpieces = ID.split("-")

        #step 1 get all known achieveements and put into Key Value pairs
        #the key is the MD5 function of AchName + ArenaName
        query = """select md5(concat(achname,arenaname)) as hash,achName,arenaName,achieveddate from allachievements aa join playerachievement pa
        on aa.achID = pa.achID
        where playerID = %s"""
        cursor.execute(query,(ID,))
        results = cursor.fetchall()
        knownAchievements = {}
        if results is not None and len(results) != 0: #new player handling 
            for knownAchievement in results:
                knownAchievements[knownAchievement[0]] = knownAchievement

        #step 2 - get all achievements from IPL
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

                __heartbeat(jobID,lastHeartbeat,playerCounter,startTime,totalPlayerCount,ID)
                #addPlayerAchievementScore(ID,centre["score"])
                #print (allAchievements)
                for achievement in centre["achievements"]:
        #step3 - for each achievement, hash it, test if we have it
        #if we have it, test if the player needs updated
        #if the player needs updated, update
        #if we don't have it, add it, and update the player.
                    tohash = "%s%s" % (achievement["name"],centre['name'])
                    tohash = tohash.encode(encoding = "utf-8")

                    md5value = hashlib.md5(tohash).hexdigest()
                    if md5value in knownAchievements: #seen it before!
                        totest = knownAchievements[md5value][3]
                        if totest == None:
                            totest = "0000-00-00"
                        if achievement["achievedDate"] != "%s" % (totest):#player has achieved / learned about this achieve!
                            addPlayerAchievement(md5value,ID,achievement["newAchievement"],achievement["achievedDate"],achievement["progressA"],achievement["progressB"])
                            DBG("updated player progress for known achievement %s vs %s" % (achievement["achievedDate"],totest),3)
            
                    else:   #new achievement!     
                        newAchMD5 = addAchievement(achievement["name"],achievement["description"],achievement["image"], centre['name'])
                        addPlayerAchievement(newAchMD5,ID,achievement["newAchievement"],achievement["achievedDate"],achievement["progressA"],achievement["progressB"])
                        DBG("updated player progress for NEW achievement: [%s][%s]" % (achievement["name"],centre['name']),3)
                    
                totalAchievemnts = totalAchievemnts + len(centre["achievements"])
            print ("Updated %i achievements for player %s. [%i/%i]" % (totalAchievemnts,ID,playerCounter,totalToUpdate))
        playerCounter = playerCounter + 1
    jobEnd(jobID)
        
    endTime = datetime.datetime.now()
    f = open("Stats.txt","a+")
    f.write("Queried {0} players' achievements, operation completed after {1}. \t\n".format(len(targetIDs),endTime - startTime ))
    f.close()

def manualTargetAchievements(targetID):
    fetchAllAchievements([targetID])


def __heartbeat(jobID,lastHeartbeat,playerCounter,startTime,totalPlayerCount,ID):
        if jobID != None:
            heartbeatDelta = (datetime.datetime.now() - lastHeartbeat).total_seconds()
            if heartbeatDelta > 30:
                jobHeartbeat(jobID,playerCounter)
                lastHeartbeat = datetime.datetime.now()
            
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
        
#manualTargetAchievements ("9-6-106")
#manualTargetAchievements ("7-2-43548")