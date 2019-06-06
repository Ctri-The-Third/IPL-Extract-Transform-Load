import requests
import json
import time
import csv
import sys


def outputPlayerToConsole(json,idAsString):
    playerName = json["centre"][0]["codename"]
    playerCentre = json["centre"][0]["name"]
    playerLevel = str(int(json["centre"][0]["skillLevelNum"])+1)
    playerLevelName = json["centre"][0]["skillLevelName"]
    print ('{4} is {0} of {1}, a level {2} {3}'.format(playerName,playerCentre,playerLevel, playerLevelName,idAsString))
    
    
    with open('playerList.csv', 'a+') as outputFile:
    
    
        limit = len(json['centre'])
        i = 0
        while i < limit:
            outputStr = '{0},{1},{2},{3},{4},{5},{6}\n'.format(
                idAsString,
                str(json["centre"][i]["name"]),
                str(json["centre"][i]["codename"]),
                str(json["centre"][i]["joined"]),
                str(json["centre"][i]["missions"]),
                str(int(json["centre"][i]["skillLevelNum"])+1),
                str(json["centre"][i]["skillLevelName"])
            ).encode(sys.stdout.encoding,errors='replace')
            outputFile.write(outputStr.decode(outputFile.encoding))
            i = i + 1
        outputFile.close()


API_DetailsURL = 'http://v2.iplaylaserforce.com/memberDetails.php'
API_AchievementsURL = 'http://v2.iplaylaserforce.com/achievements.php'
API_recentMissions = 'http://v2.iplaylaserforce.com/recentMissions.php'
targetRegion = 7
targetSite = 8
targetMember = 1196 #current start

totalRequests = 1
nonResponses = 0
print("======preparing to read and write.======")
print(sys.stdout.encoding)
#while targetMember < 17500 and nonResponses <= 50: 
while (totalRequests == 1):

    data = {'requestId':str(totalRequests), 
            'regionId':'9999', 
            'siteId':'9999', 
            'memberRegion':str(targetRegion),
            'memberSite':str(targetSite),
            'memberId':str(targetMember)} 

    r = requests.post(url = API_DetailsURL, data = data)
    #print("===============\nRead Complete, response = \n"+r.text+"\n===============")
    responseJSON = json.loads(r.text)

    MemberIDAsString = "{0}-{1}-{2}".format(str(targetRegion),str(targetSite),str(targetMember))

    if 'centre'  in responseJSON and len(responseJSON['centre']) >= 1:
        outputPlayerToConsole(responseJSON,MemberIDAsString)
        nonResponses = 0
    else:
        nonResponses = nonResponses + 1
        print ("{0} was not found, this is consecutive instance {1} ".format(MemberIDAsString,nonResponses))
        

    targetMember = targetMember + 1
    totalRequests = totalRequests + 1
    #time.sleep(0)





#for  i in range(len(json["centre"])) :
#    print(json["centre"][i])
#    i += 1
