from SQLconnector import connectToSource
import ConfigHelper
import json
import os
from DBG import DBG
conn = connectToSource()
cursor = conn.cursor()

#sqlfile = open("/home/ctri/github/LF-Profiler/SQL Queries/PlayerQuality-Big5-allYearByMonth.sql")
#SQL = sqlfile.read()#.replace('', '')
def execute():
    SQL = """
     with starQuality as
 (
	select playerID, gamertag
	,avg(starsforgame) as avgQualityPerGame 
	,gamemonth
	,count(*) as gamesPlayed 
	from public."participationWithStars"
	where gameTimestamp >= %s
	and gameTimestamp < %s
	and arenaName ilike %s
	group by 1,2,4
    ),
    GoldenTopX as 
    (
        select PlayerID, gamertag
        , ROW_NUMBER() over (partition by gameMonth order by avgQualityPerGame desc) as playerRank 
        , gameMonth
        from StarQuality
        where StarQuality.gamesPlayed >= 3
        order by AvgQualityPerGame desc
        --limit 3 
    ),
    GoldenTop3 as 
    ( 
        select * from GoldenTopX
       where playerRank <= 3
    )
    
    select * from GoldenTop3 g3  join StarQuality sq on
    sq.playerID = g3.playerID and 
    sq.gameMonth = g3.gameMonth
    order by g3.gameMonth asc, g3.playerRank asc 

   
    """
    #--startDate,endDate, siteNameReal, name (sen) (sen) (sen) name
    cfg = ConfigHelper.getConfig()

    startYear = int(cfg["StartDate"][0:4])
    endYear = startYear + 1

    startYear = "%s-01-01" % startYear
    endYear = "%s-01-01" % endYear
    #startYear = '2019-08-01'
    parameters = (
        startYear, endYear, cfg['SiteNameReal']
        , cfg['SiteNameReal']
        , startYear, endYear, cfg['SiteNameReal']
        , startYear, endYear, cfg['SiteNameReal']
        , startYear, endYear, cfg['SiteNameReal']
        , cfg['SiteNameReal'])
    conn = connectToSource()
    cursor = conn.cursor()

    cursor.execute(SQL,parameters)
    results = cursor.fetchall()
    SQLdesc = cursor.description
    descCount = 0
    for desc in SQLdesc:
        #print("%s %s" % (descCount,desc[0]))
        descCount = descCount + 1

    currentMonth = ""
    months = []
    for result in results:
        
        if result [2] != currentMonth:
            currentMonth = result[2]
            #print("== New month = [%s]" % (currentMonth,))
            month = {}
            months.append(month)
            month["month"] = result[2]
            players = []
            month["players"] = players
            
        #print(result)
        player = {}
        player["playerName"] = result[4]
        player["gamePlayed"] = result[6]
        player["averageStars"] = "%s" % (result[8])
        players.append(player)
        playerName = "%s%s" % (result[4]," "*15)
        playerName = playerName[0:10]
        #print("%s %s, %s games played \t %s stars per game (avg) " % (result[1],playerName , result[6], result[8]) )

    #print(json.dumps(months,indent=4))
    #playerID, rank, month, 
    #ID, gamertag, avgopponents
    #gamesplayed, averagerank, avgqual
    #totalqual, avgscore, achievementscore
    #gamemonth

    filepart = "AnnualTop3s" 
    if os.name == "nt":
        divider = "\\" 
    elif os.name == "posix":
        divider = "/"
    f = open("JSONBlobs%s%s%s-%s.json" % (divider, cfg["ID Prefix"],filepart,startYear[0:4]), "w+")
    f.write(json.dumps(months,indent=4))
    DBG ("Annual top3s complete!",3)
