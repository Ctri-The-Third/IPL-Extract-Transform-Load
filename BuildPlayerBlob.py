import requests
import json
import importlib

from FetchUsers import fetchPlayer_root
from FetchUsers import fetchPlayerAcheivement_root

r = []

dataOut = {}
dataOut['basicInfo'] = fetchPlayer_root('',9,6,106)
dataOut['achievements']  = fetchPlayerAcheivement_root('',9,6,106)
dataOut['recentGames'] = {}

with open('playerBlob.json', 'w+') as outputFile:
    outputFile.write(json.dumps(dataOut, indent=4))
    outputFile.close()

#print(r)
for i in r:
    codename = i["centre"][0]["codename"]
    missionsCount = i["centre"][0]["missions"]
    level = str(int(i["centre"][0]["skillLevelNum"])+1)
    levelN = i["centre"][0]["skillLevelName"]
    averageScore = i["centre"][0]["summary"][0][4]
    lastplayed = i["centre"][0]["summary"][0][2]

    print ("{0} is a Level {2} {3}, and has played {1} missions at their home arena.\n Their average score is {4} and they last played at their home arena on {5} \n"
    .format(codename,missionsCount,level,levelN,averageScore,lastplayed))


#r["centre"][0]["name"] #global Achievements
#r["centre"][1]["name"] #Funstation Ltd, Edinburgh, Scotland
#print ( r["centre"][1]["achievements"][0]["name"] ) #Lurker

