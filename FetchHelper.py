import requests
import json
import time
import csv
import sys



def outputPlayerToCSV(json,idAsString):
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


def fetchPlayer_token(token):
    return fetchPlayer_root(token,'','','')
    
def fetchPlayer_ID(region,site,code):
    return fetchPlayer_root('',region,site,code)

def fetchPlayer_root(token,region,site,code):

    API_DetailsURL = 'http://v2.iplaylaserforce.com/memberDetails.php'
    

    data = {'requestId':str(1), 
            'regionId':'9999', 
            'siteId':'9999', 
            'memberRegion':str(region),
            'memberSite':str(site),
            'memberId':str(code),
            'token':str(token)} 

    r = requests.post(url = API_DetailsURL, data = data)
    
    responseJSON = json.loads(r.text)
    if 'centre'  in responseJSON and len(responseJSON['centre']) >= 1:
        
        print("fetchPlayer_root: Found player %s-%s-%s, token %s" % (region,site,code,token))
        return (responseJSON)
    else:
        print("fetchPlayer_root: DIDN'T find player %s-%s-%s, token %s" % (region,site,code,token))
        return ()

def fetchPlayerAcheivement_root(token,region,site,code):
    API_AchievementsURL = 'http://v2.iplaylaserforce.com/achievements.php'
    
    data = {'requestId':str(1), 
    'regionId':'9999', 
    'siteId':'9999', 
    'memberRegion':str(region),
    'memberSite':str(site),
    'memberId':str(code),
    'token':str(token)} 

    r = requests.post(url = API_AchievementsURL, data = data)
    #print (r.text)
    responseJSON = json.loads(r.text)
    #print (responseJSON)
    if 'centre'  in responseJSON and len(responseJSON['centre']) >= 1:
        
        return (responseJSON)
    else:
        return ()


def fetchPlayerRecents_root(token,region,site,code):
    API_recentMissions = 'http://v2.iplaylaserforce.com/recentMissions.php'
    data = {'requestId':str(1), 
            'regionId':'9999', 
            'siteId':'9999', 
            'memberRegion':str(region),
            'memberSite':str(site),
            'memberId':str(code),
            'token':str(token)} 

    r = requests.post(url = API_recentMissions, data = data)
    
    responseJSON = json.loads(r.text)
    if 'mission'  in responseJSON and len(responseJSON['mission']) >= 1:
        
        return (responseJSON)
    else:
        return ()
#================ begins the actual looping and scraping here
'''
targetRegion = 7
targetSite = 8
targetMember = 1196 #current start

totalRequests = 1
nonResponses = 0

#while targetMember < 17500 and nonResponses <= 50: 
while (totalRequests == 1):

    #MemberIDAsString = "{0}-{1}-{2}".format(str(targetRegion),str(targetSite),str(targetMember))
    json = fetchPlayer_ID(targetRegion,targetSite,targetMember)
    
    targetMember = targetMember + 1
    totalRequests = totalRequests + 1
'''

#print ("====Testing FetchUsers with user 9-6-106====")
#fetchPlayer_root('',9,6,106)
#fetchPlayerRecents_root('',9,6,106)