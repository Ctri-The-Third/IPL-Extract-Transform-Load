import requests
import json
import time
import csv



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
            )
            outputFile.write(outputStr)
            i = i + 1
        outputFile.close()


API_DetailsURL = 'http://v2.iplaylaserforce.com/memberDetails.php'
API_AchievementsURL = 'http://v2.iplaylaserforce.com/achievements.php'
API_recentMissions = 'http://v2.iplaylaserforce.com/recentMissions.php'
targetRegion = 7
targetSite = 9
targetMember = 186 #current start


while targetMember < 30000: 

    data = {'requestId':'1', 
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
    else:
        print ("Did not find player: {0}".format(MemberIDAsString))

    targetMember = targetMember + 1
    time.sleep(1)





#for  i in range(len(json["centre"])) :
#    print(json["centre"][i])
#    i += 1