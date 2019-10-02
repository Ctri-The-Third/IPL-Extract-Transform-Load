from DBG import DBG
import math 
import datetime
import string 
import colorama
import queue
import time 
from colorama import Fore, Back
from SQLconnector import connectToSource
from SQLHelper import addPlayer
from FetchHelper import fetchPlayer_root
import workerProgressQueue as wpq
import ConfigHelper as cfg 
from psycopg2 import sql 

def findNewPlayers():
    startTime = datetime.datetime.now()
    conn = connectToSource()
    cursor = conn.cursor()

    conn = connectToSource()
    cursor = conn.cursor()
    sitePrefix = cfg.getConfigString("ID Prefix")
    siteName = cfg.getConfigString("SiteNameReal")
    TickerIcon = ["|","/","-",'\\']
#
    query = sql.SQL("""
 with PlayerSegments as (
 	select distinct cast( split_part(pl.PlayerID,'-',3) as INTEGER) as IDSuffix
	from players pl join Participation p on pl.PlayerID = p.PlayerID
    join games g on p.GameUUID = g.GameUUID
    where g.ArenaName = '%s'  )

 select max (IDSuffix) from PlayerSegments where  IDSuffix < 100000
    
    """).format(siteName)
    cursor.execute(query)
    result = cursor.fetchone()
    if result[0] == None:
        MaxPlayer = 199 #LaserForce seems to start numbering players at 100
    else: 
        MaxPlayer = result[0]
        #MaxPlayer = 38100 #LaserForce seems to start numbering players at 100
    region = sitePrefix.split("-")[0]
    siteNumber = sitePrefix.split("-")[1]

    
    #MaxPlayer = 243 #OVERRIDE, remove before committing
    ticker = 0
    consecutiveMisses = 0
    currentTarget = MaxPlayer - 100 #we've had situations where the system adds user IDs behind the maximum. This is a stopgap dragnet to catch trailing players.
    AllowedMisses = 100
    while consecutiveMisses <= AllowedMisses:
        player =  fetchPlayer_root('',region,siteNumber,currentTarget)
        if 'centre' in player:
            
            codeName = player["centre"][0]["codename"]
            dateJoined = player["centre"][0]["joined"]
            missionsPlayed = player["centre"][0]["missions"]
            skillLevelNum = player["centre"][0]["skillLevelNum"]
            addPlayer("%s%i" % (sitePrefix,currentTarget),codeName,dateJoined,missionsPlayed,skillLevelNum)
            consecutiveMisses = 0
        else: 
            DBG("DBG: FetchPlayerUpdatesAndNewPlayers.findNewPlayers - Missed a player 7-X-%s" % (currentTarget),3)
            consecutiveMisses = consecutiveMisses + 1
        wpq.updateQ(consecutiveMisses,AllowedMisses,"Seeking new... %s" % TickerIcon[ticker % 4],"ETA ?")    
        currentTarget = currentTarget + 1 
        ticker = ticker + 1
        
    endTime = datetime.datetime.now()
    f = open("Stats.txt","a+")
    
    f.write("searched for {0} players, operation completed after {1}. \t\n".format(currentTarget-MaxPlayer,endTime - startTime ))
    wpq.updateQ(1,1,"Seeking new... %s","Complete")
    f.close()
    conn.commit()
    conn.close()
def updateExistingPlayers():
    startTime = datetime.datetime.now()
    conn = connectToSource()
    cursor = conn.cursor()


    query = """with data as ( select row_number() over (order by Level desc, Missions desc) as ID, PlayerID, Missions, Level from Players)
	select PlayerID from data
            where (ID >= 0)
			order by ID asc 
            """
    cursor.execute(query)
    results = cursor.fetchall()

    totalTargetsToUpdate = len(results)
    counter = 0
    global WorkerStatus
    for result in results:
        
        counter = counter + 1
        WorkerStatus = {}
        WorkerStatus["CurEntry"] = counter
        WorkerStatus["TotalEntries"] = totalTargetsToUpdate
        WorkerStatus["CurrentAction"] = "summary of %s" % (result[0]) 
        delta = "[    Calculating     ]"
        if counter >= 20:
            delta = ((datetime.datetime.now() - startTime).total_seconds() / counter) 
            delta = (totalTargetsToUpdate - counter) * delta #seconds remaining
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
            
        wpq.updateQ(counter,totalTargetsToUpdate,"summary of %s" % (result[0]) ,delta)
            
        

        ID = result[0].split('-')
        player = fetchPlayer_root('',ID[0],ID[1],ID[2])

        datetime_list = []
        missions = 0
        level = 0
        for i in player["centre"]:
            datetime_list.append (str(i["joined"]))
            missions += int(i["missions"])
            level = max(level,int(i["skillLevelNum"]))
        joined = min(datetime_list)
        codeName = str(player["centre"][0]["codename"])


        #print("Summary update for player %s-%s-%s, [%i/%i]" % (ID[0],ID[1],ID[2],counter,totalTargetsToUpdate))
        addPlayer(result[0],codeName,joined,missions,level)

    endTime = datetime.datetime.now()
    f = open("Stats.txt","a+")
    f.write("Queried {0} players' aggregates, operation completed after {1}. \t\n".format(len(results),endTime - startTime ))
    f.close()

def manualTargetSummary(rootID):
    ID = rootID.split('-')
    player = fetchPlayer_root('',ID[0],ID[1],ID[2])
    if player == {}:
        DBG("ManualTargetSummary failed! Aborting",1)
        return
    print("Manual update of player sumary complete")
    addPlayer(rootID,player["centre"][0]["codename"],player["centre"][0]["joined"],player["centre"][0]["missions"],player["centre"][0]["skillLevelNum"])



 