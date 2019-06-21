import datetime
import string 

from SQLconnector import connectToSource
from SQLHelper import addPlayer
from FetchHelper import fetchPlayer_root


def findNewPlayers():
    conn = connectToSource()
    cursor = conn.cursor()



    query = """
    select max(CONVERT(int,SUBSTRING(PlayerID,5,20))) as MaxPlayerID
    from players
    where SUBSTRING(PlayerID,1,4) = '7-9-'                  --only locals
    and CONVERT(int,SUBSTRING(PlayerID,5,20)) < 100000      --not players with messed up cards
    """
    results = cursor.execute(query)
    result = results.fetchone()
    if result == None:
        MaxPlayer = 99 #LaserForce seems to start numbering players at 100
    else: 
        MaxPlayer = result[0]
    conn.commit()
    conn.close()
def updateExistingPlayers():
    startTime = datetime.datetime.now()
    conn = connectToSource()
    cursor = conn.cursor()

    query = """select PlayerID from Players"""
    results = cursor.execute(query)
    for result in results:
        ID = result[0].split('-')
        player = fetchPlayer_root('',ID[0],ID[1],ID[2])
        #print(player)
        addPlayer(result[0],player["centre"][0]["codename"],player["centre"][0]["joined"],player["centre"][0]["missions"],player["centre"][0]["skillLevelNum"])
    endTime = datetime.datetime.now()
    f = open("Stats.txt","a+")
    f.write("Queried {0} players' aggregates, operation completed after {1}. \t\n".format(len(results),endTime - startTime ))
    f.close()
updateExistingPlayers()
