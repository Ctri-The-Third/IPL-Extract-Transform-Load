import requests
import json
import importlib
import datetime

from FetchUsers import fetchPlayer_root
from FetchUsers import fetchPlayerRecents_root
from SQLconnector import addPlayer

targetIDs = {
    '9-6-106', #C'tri
}

for ID in targetIDs:
    region = ID.split("-")[0]
    site =  ID.split("-")[1]
    IDPart = ID.split("-")[2]
    print("DBG: %s-%s-%s" % (region,site,IDPart))
    summaryJson = fetchPlayer_root('',region,site,IDPart)
    if summaryJson is not None:
        datetime_list = []
        missions = 0
        for i in summaryJson["centre"]:
            datetime_list.append (str(i["joined"]))
            missions += int(i["missions"])
        joined = min(datetime_list)
        codeName = str(summaryJson["centre"][0]["codename"])
        addPlayer(ID,codeName,joined,missions)
    
        missionsJson = fetchPlayerRecents_root('',region,site,IDPart)
        print("Fetched missions played JSON")
        
    else:
        print("Didn't find %s" % ID)

#iterate through the above and fetch stats for all.
#iterate through all players received and update / import player info
#iterate through all games played and create game records, and player associations.