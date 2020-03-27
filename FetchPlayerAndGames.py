import math 
import requests
import json
import importlib
import datetime
import queue
from colorama import Fore
from FetchHelper import fetchPlayer_root
from FetchHelper import fetchPlayerRecents_root
from SQLHelper import addPlayer
from SQLHelper import addGame 
from SQLHelper import addParticipation
from SQLHelper import getInterestingPlayersRoster
from SQLHelper import jobStart, jobHeartbeat, jobEnd
import ConfigHelper as cfg
import workerProgressQueue as wpq 
import DBG 

 #The query starts at the date in question and looks backwards. We use the "End Date" from the config.
#targetIDs = getInterestingPlayersRoster(False,cfg.getConfigString("EndDate'],cfg.getConfigString("ChurnDuration'])


#targetIDs = {
#    '7-8-0839' 
#}
updatedPlayers = []

def QueryGamesLoad(scope, interval = "Null", ArenaName = None, offset = None, ID = None):
    params = {}
    params["scope"] = scope
    params["arenaName"] = cfg.getConfigString("SiteNameReal")
    if scope == "full": 
        targetIDs = getInterestingPlayersRoster(True,cfg.getConfigString("StartDate"),cfg.getConfigString("ChurnDuration"),offset=offset)
        if ID == None: #new job
            ID = jobStart("Fetch games, all players",0,"FetchPlayerAndGames.executeQueryGames",params,len(targetIDs),delay=-2)
    elif scope == "activePlayers":
        targetIDs = getInterestingPlayersRoster(False,cfg.getConfigString("StartDate"),cfg.getConfigString("ChurnDuration"),offset=offset,siteName =  None)
        if ID == None: #new job
            ID = jobStart("Fetch games, All arenas active players " ,0,"FetchPlayerAndGames.executeQueryGames",params,len(targetIDs), delay=-2) 
    else: #local
        targetIDs = getInterestingPlayersRoster(False,cfg.getConfigString("StartDate"),cfg.getConfigString("ChurnDuration"),offset=offset,siteName = params["arenaName"])
        if ID == None: #new job
            ID = jobStart("Fetch games, [%s] active players " % (cfg.getConfigString("SiteNameShort")),0,"FetchPlayerAndGames.executeQueryGames",params,len(targetIDs), delay=-2) 
            
    for targetID in targetIDs:
        wpq.gamesQ.put(targetID)
    
    return ID


def QueryGamesExecute(scope, interval = "Null", ArenaName = None, offset = None, ID = None): #Scope should be "full" or "partial"
    jobID = QueryGamesLoad(scope,interval, ArenaName,offset,ID)
    #QueryGamesLoop(jobID,offset)

def queryIndividual(ID, scope = None):
        
    region = ID.split("-")[0]
    site =  ID.split("-")[1]
    IDPart = ID.split("-")[2]
    
    summaryJson = fetchPlayer_root('',region,site,IDPart)
    if summaryJson is not None:
        #print(DBGstring)
        datetime_list = []
        missions = 0
        level = 0
        for i in summaryJson["centre"]:
            datetime_list.append (str(i["joined"]))
            missions += int(i["missions"])
            level = max(level,int(i["skillLevelNum"]))
        joined = min(datetime_list)
        codeName = str(summaryJson["centre"][0]["codename"])
        playerNeedsUpdated = addPlayer(ID,codeName,joined,missions)

        
        if playerNeedsUpdated == True or scope == "full":
            updatedPlayers.append(ID)
            missionsJson = fetchPlayerRecents_root('',region,site,IDPart)
            if missionsJson != None:
                for mission in missionsJson["mission"]:
                
                    missionUUID = addGame(mission[0],mission[1],mission[2])
                    "FetchPlayerAndGames: %s, %s " % (missionUUID, mission)
                    addParticipation(missionUUID,ID,mission[3])
    
def QueryGamesLoop (jobID,counter = 0):
     
    jobHeartbeat(jobID,counter)
    totalPlayerCount = wpq.gamesQ.qsize() + counter
    startTime = datetime.datetime.now()
    lastHeartbeat = startTime
    global WorkerStatus
    while wpq.gamesQ.empty() == False:
        ID = wpq.gamesQ.get()
        ETA = "Calculating"
        if  jobID != None:
            heartbeatDelta = ((datetime.datetime.now() - lastHeartbeat).total_seconds()) 
            if heartbeatDelta > 30 or counter % 5 == 0:
                jobHeartbeat(jobID,counter)
                lastHeartbeat = datetime.datetime.now()
        if counter >= 20:
            delta = ((datetime.datetime.now() - startTime).total_seconds() / counter) 
            delta = (totalPlayerCount - counter) * delta #seconds remaining
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

        
        DBGstring = "Seeking games for %s, [%i / %i] : " % (ID,counter,totalPlayerCount)
        DBG.DBG(DBGstring,2)
        wpq.updateQ(counter,totalPlayerCount, "games for %s" % (ID),ETA)
        counter = totalPlayerCount - wpq.gamesQ.qsize() 
        queryIndividual(ID)
        wpq.gamesQ.task_done()
    jobEnd(jobID)        


    endTime = datetime.datetime.now()
    #f = open("Stats.txt","a+")
    #f.write("Queried {0} players' recent games, operation completed after {1}. \t\n".format(len(targetIDs),endTime - startTime ))
    #f.close()

def manualTargetForGames(targetID):
    queryIndividual(targetID,"individual")
 

