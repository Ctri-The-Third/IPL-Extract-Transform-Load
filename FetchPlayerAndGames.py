import requests
import json
import importlib
import datetime

from FetchHelper import fetchPlayer_root
from FetchHelper import fetchPlayerRecents_root
from SQLHelper import addPlayer
from SQLHelper import addGame
from SQLHelper import addParticipation
from SQLHelper import getInterestingPlayersRoster

targetIDs = getInterestingPlayersRoster()


#targetIDs = {
#    '7-8-0839'
#}

startTime = datetime.datetime.now()
for ID in targetIDs:
    region = ID.split("-")[0]
    site =  ID.split("-")[1]
    IDPart = ID.split("-")[2]
    print("DBG: %s-%s-%s" % (region,site,IDPart))
    summaryJson = fetchPlayer_root('',region,site,IDPart)
    if summaryJson is not None:
        datetime_list = []
        missions = 0
        level = 0
        for i in summaryJson["centre"]:
            datetime_list.append (str(i["joined"]))
            missions += int(i["missions"])
            level = max(level,int(i["skillLevelNum"]))
        joined = min(datetime_list)
        codeName = str(summaryJson["centre"][0]["codename"])
        addPlayer(ID,codeName,joined,missions,level)
    
        missionsJson = fetchPlayerRecents_root('',region,site,IDPart)
        for mission in missionsJson["mission"]:
            
            missionUUID = addGame(mission[0],mission[1],mission[2])
            "FetchPlayerAndGames: %s, %s " % (missionUUID, mission)
            addParticipation(missionUUID,ID,mission[3])
    else:
        print("Didn't find %s" % ID)

endTime = datetime.datetime.now()
f = open("Stats.txt","a+")
f.write("Queried {0} players' recent games, operation completed after {1}. \t\n".format(len(targetIDs),endTime - startTime ))
f.close()