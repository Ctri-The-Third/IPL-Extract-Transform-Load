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
 

 #The query starts at the date in question and looks backwards. We use the "End Date" from the config.
#targetIDs = getInterestingPlayersRoster(False,cfg.getConfigString("EndDate'],cfg.getConfigString("ChurnDuration'])


#targetIDs = {
#    '7-8-0839' 
#}
updatedPlayers = []

def executeQueryGames(scope, interval = "Null", ArenaName = None, offset = None, ID = None): #Scope should be "full" or "partial"
    params = {}
    params["scope"] = scope
    params["arenaName"] = cfg.getConfigString("SiteNameReal")
    if scope == "full": 
        targetIDs = getInterestingPlayersRoster(True,cfg.getConfigString("StartDate"),cfg.getConfigString("ChurnDuration"),offset=offset)
        if ID == None: #new job
            ID = jobStart("Fetch games, all players",0,"FetchPlayerAndGames.executeQueryGames",params)
    else: 
        targetIDs = getInterestingPlayersRoster(False,cfg.getConfigString("StartDate"),cfg.getConfigString("ChurnDuration"),offset=offset,siteName = params["arenaName"])
        if ID == None: #new job
            ID = jobStart("Fetch games, [%s] active players " % (cfg.getConfigString("SiteNameShort")),0,"FetchPlayerAndGames.executeQueryGames",params) 
            
    queryPlayers(targetIDs,scope, siteName = params["arenaName"], jobID=ID, offset=offset)

def queryPlayers (targetIDs,scope, siteName = None, jobID = None, offset = None):
    updatedPlayers = []
    
    counter = 0
    if offset is not None:
        counter = offset
    totalPlayerCount = len(targetIDs) + counter
    startTime = datetime.datetime.now()
    lastHeartbeat = startTime
    global WorkerStatus
    for ID in targetIDs:
        ETA = "Calculating"
        if  jobID != None:
            heartbeatDelta = ((datetime.datetime.now() - lastHeartbeat).total_seconds()) 
            if heartbeatDelta > 30:
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

        counter = counter + 1 
        
        region = ID.split("-")[0]
        site =  ID.split("-")[1]
        IDPart = ID.split("-")[2]
        
        DBGstring = "Seeking games for %s-%s-%s, [%i / %i] : " % (region,site,IDPart,counter,totalPlayerCount)
        wpq.updateQ(counter,totalPlayerCount, "games for %s-%s-%s" % (region,site,IDPart),ETA)
        
        
        
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
            playerNeedsUpdated = addPlayer(ID,codeName,joined,missions,level)
            
            if playerNeedsUpdated != 0 or scope == "full":
                updatedPlayers.append(ID)
                missionsJson = fetchPlayerRecents_root('',region,site,IDPart)
                if missionsJson != None:
                    for mission in missionsJson["mission"]:
                 
                        missionUUID = addGame(mission[0],mission[1],mission[2])
                        "FetchPlayerAndGames: %s, %s " % (missionUUID, mission)
                        addParticipation(missionUUID,ID,mission[3])
        else:
            DBGstring += "WARNING no data received for user."
            #print(DBGstring)
            
    jobEnd(jobID)        


    endTime = datetime.datetime.now()
    f = open("Stats.txt","a+")
    f.write("Queried {0} players' recent games, operation completed after {1}. \t\n".format(len(targetIDs),endTime - startTime ))
    f.close()

def manualTargetForGames(targetID):
    queryPlayers([targetID],"full")
 

