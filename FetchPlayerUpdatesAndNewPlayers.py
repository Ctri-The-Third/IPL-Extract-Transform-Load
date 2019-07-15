import datetime
import string 

from SQLconnector import connectToSource
from SQLHelper import addPlayer
from FetchHelper import fetchPlayer_root
from ConfigHelper import getConfig


def findNewPlayers():
    startTime = datetime.datetime.now()
    conn = connectToSource()
    cursor = conn.cursor()

    conn = connectToSource()
    cursor = conn.cursor()
    config = getConfig()
    sitePrefix = config["ID Prefix"]


    query = """
    select max(CONVERT(int,SUBSTRING(PlayerID,5,20))) as MaxPlayerID
    from players
    where SUBSTRING(PlayerID,1,4) = ?                       --only locals
    and CONVERT(int,SUBSTRING(PlayerID,5,20)) < 100000      --not players with messed up cards
    """
    results = cursor.execute(query,(sitePrefix))
    result = results.fetchone()
    if result == None:
        MaxPlayer = 99 #LaserForce seems to start numbering players at 100
    else: 
        MaxPlayer = result[0]


    #MaxPlayer = 243 #OVERRIDE, remove before committing
    consecutiveMisses = 0
    currentTarget = MaxPlayer
    while consecutiveMisses <= 50:
        player =  fetchPlayer_root('',7,9,currentTarget)
        if 'centre' in player:
            
            codeName = player["centre"][0]["codename"]
            dateJoined = player["centre"][0]["joined"]
            missionsPlayed = player["centre"][0]["missions"]
            skillLevelNum = player["centre"][0]["skillLevelNum"]
            addPlayer("%s%i" % (sitePrefix,currentTarget),codeName,dateJoined,missionsPlayed,skillLevelNum)
            consecutiveMisses = 0
        else: 
            consecutiveMisses = consecutiveMisses + 1
        currentTarget = currentTarget + 1 
    endTime = datetime.datetime.now()
    f = open("Stats.txt","a+")
    
    f.write("searched for {0} players, operation completed after {1}. \t\n".format(currentTarget-MaxPlayer,endTime - startTime ))
    f.close()
    conn.commit()
    conn.close()
def updateExistingPlayers():
    startTime = datetime.datetime.now()
    conn = connectToSource()
    cursor = conn.cursor()

    query = """select PlayerID, Missions, Level from Players
            order by Level desc, Missions desc"""
    results = cursor.execute(query).fetchall()
    totalTargetsToUpdate = len(results)
    counter = 0
    for result in results:
        counter = counter + 1
        ID = result[0].split('-')
        player = fetchPlayer_root('',ID[0],ID[1],ID[2])
        print("Summary update for player %s-%s-%s, [%i/%i]" % (ID[0],ID[1],ID[2],counter,totalTargetsToUpdate))
        addPlayer(result[0],player["centre"][0]["codename"],player["centre"][0]["joined"],player["centre"][0]["missions"],player["centre"][0]["skillLevelNum"])
    endTime = datetime.datetime.now()
    f = open("Stats.txt","a+")
    f.write("Queried {0} players' aggregates, operation completed after {1}. \t\n".format(len(results),endTime - startTime ))
    f.close()

def manualTargetSummary(rootID):
    ID = rootID.split('-')
    player = fetchPlayer_root('',ID[0],ID[1],ID[2])
    print("Manual update of player sumary complete")
    addPlayer(rootID,player["centre"][0]["codename"],player["centre"][0]["joined"],player["centre"][0]["missions"],player["centre"][0]["skillLevelNum"])

