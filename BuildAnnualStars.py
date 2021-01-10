from SQLconnector import connectToSource
import ConfigHelper
import json
import os
from DBG import DBG






def executeBuild_AnnualStars():
    conn = connectToSource()
    cursor = conn.cursor()

    outputObject = {}

    cfg = ConfigHelper.getConfig()
    startYear = int(cfg["StartDate"][0:4])
    endYear = startYear + 1
    startYear = "%s-01" % startYear
    endYear = "%s-01" % endYear
    arena = cfg["SiteNameReal"]

    SQL = """with subsetOfData as 
(
	select playerID
	, gamerTag
	, avg(playercount) as AveragePlayerCount
	, count(*) as GamesPlayed
	, avg(Starsforgame) as AverageStarQuality
	, sum(Starsforgame) as TotalStarQuality
	, avg(rank) as AverageRank 
	from public."participationWithStars"
	where arenaName ilike %s
	and GameMonth >= %s and gameMonth <= %s
	group by 1,2
)

select r1.PlayerID, r1.GamerTag,
round (cast(r1.AverageStarQuality as numeric),2) as AverageStarQuality, 
round (cast(r1.AverageStarQuality * r1.gamesPlayed as numeric),2) as TotalStarQuality,
round (cast(r1.AveragePlayerCount as numeric),2) as AveragePlayerCount, 
round (cast(r1.AverageRank as numeric),2) as AverageRank, 
r1.gamesPlayed as GamesPlayed
from subsetOfData r1 
order by AverageStarQuality desc
limit 50 """

    parameters = [arena,startYear,endYear]
    cursor.execute(SQL,parameters)
    results = cursor.fetchall()

    brightStars = []
    for result in results:
        player = {}
        player["gamertag"] = result[1]
        player["averageStars"] = "%s" % (result[2])
        player["averageOpponents"] = "%s" % ( result[4])
        player["averageRank"] = "%s" % ( result[5])
        player["gamesPlayed"] = "%s" % ( result[6])
        brightStars.append(player)
    

    outputObject["brightestStars"] = brightStars





    SQL = """with subsetOfData as 
(
	select playerID
	, gamerTag
	, avg(playercount) as AveragePlayerCount
	, count(*) as GamesPlayed
	, avg(Starsforgame) as AverageStarQuality
	, sum(Starsforgame) as TotalStarQuality
	, avg(rank) as AverageRank 
	from public."participationWithStars"
	where arenaName ilike %s
	and GameMonth >= %s and gameMonth <= %s
	group by 1,2
)

select r1.PlayerID, r1.GamerTag,
round (cast(r1.AverageStarQuality as numeric),2) as AverageStarQuality, 
round (cast(r1.AverageStarQuality * r1.gamesPlayed as numeric),2) as TotalStarQuality,
round (cast(r1.AveragePlayerCount as numeric),2) as AveragePlayerCount, 
round (cast(r1.AverageRank as numeric),2) as AverageRank, 
r1.gamesPlayed as GamesPlayed
from subsetOfData r1 
order by TotalStarQuality desc
limit 50 """

    parameters = [arena,startYear,endYear]
    cursor.execute(SQL,parameters)
    results = cursor.fetchall()

    players = []
    for result in results:
        player = {}
        player["gamertag"] = result[1]
        player["averageStars"] = "%s" % (result[3])
        player["averageOpponents"] = "%s" % ( result[4])
        player["averageRank"] = "%s" % ( result[5])
        player["gamesPlayed"] = "%s" % ( result[6])
        players.append(player)
   
    outputObject["biggestStars"] = players


    filepart =  "AnnualStars" 
    if os.name == "nt":
        divider = "\\" 
    elif os.name == "posix":
        divider = "/"
    f = open("JSONBlobs%s%s%s-%s.json" % (divider, cfg["ID Prefix"],filepart,startYear[0:4]), "w+")
    f.write(json.dumps(outputObject,indent=4))
    DBG ("Annual Brightest Stars complete complete!",3)

