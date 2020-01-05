from SQLconnector import connectToSource
import ConfigHelper
import json
import os
from DBG import DBG
conn = connectToSource()
cursor = conn.cursor()

outputObject = {}

#topGames
print ("  == Which games were played")

SQL = """
select count(*), gamename from games g 
where arenaName ilike %s
and gametimestamp >= %s
and gametimestamp <= %s
group by 2
order by 1 desc;
"""
cfg = ConfigHelper.getConfig()

parameters = (
      cfg['SiteNameReal'], cfg['StartDate'], cfg['EndDate']
      )
conn = connectToSource()
cursor = conn.cursor()

cursor.execute(SQL,parameters)
results = cursor.fetchall()
SQLdesc = cursor.description
descCount = 0

for desc in SQLdesc:
    #print("%s %s" % (descCount,desc[0]))
    descCount = descCount + 1

gamesPlayed = []
for result in results:
    print (result)
    game = {'gameName' : result[1], 'timesPlayed' : result[0] }
    gamesPlayed.append(game)
outputObject['gamesPlayed'] = gamesPlayed
#referrals
print ("  == Referrals and Welcomers")

SQL = """

with firstGames as 
(
	select gamerTag, p.playerID, min(gametimestamp) as firstGame
	from players pl 
	join participation p on p.playerID = pl.playerID
	join games g  on p.gameuuid = g.gameuuid
	group by 2,1
),
playersInGames as 
(
	select count(*) as countOfPlayersInGame, gametimestamp
	from players pl
	join participation p on p.playerID = pl.playerID
	join games g  on p.gameuuid = g.gameuuid
	group by 2
),
gamesWithNewPlayers as 
(
	select 	count (case when gametimestamp = firstgame then 1 else null end) as newPlayers
	,	count (case when gametimestamp != firstgame then 1 else null end) as existingPlayers
	,	gametimestamp
	,	arenaname
	from players pl
	join participation p on p.playerID = pl.playerID
	join games g  on p.gameuuid = g.gameuuid
	join firstGames fg on pl.playerID = fg.playerID
	where gametimestamp >= %s /*StartDate*/ and gametimestamp < %s /*EndDate*/
	and arenaname ilike %s /*SiteNameReal*/
	group by 3,4
	order by 3 desc
),
referredPlayers as 
(
	
	select pl.gamertag, g.gametimestamp, firstgame, newplayers, existingplayers,
	case when firstgame = g.gametimestamp then 'REFERRED!' else 'referee' end as referalRole
	from players pl
	join participation p on p.playerID = pl.playerID
	join games g  on p.gameuuid = g.gameuuid
	join firstGames fg on pl.playerID = fg.playerID
	join gamesWithNewPlayers gwnp on gwnp.gametimestamp = g.gametimestamp and gwnp.arenaname = g.arenaname
	where newplayers > 0 and existingPlayers > 0 
	order by g.gametimestamp desc
)
select count(distinct gamerTag), 'new player' as playerRole from referredPlayers
	where referalrole = 'REFERRED!'
union 
select count (distinct gamerTag), 'veteran' from referredPlayers
	where referalrole = 'referee'
"""


parameters = (
      cfg['StartDate'], cfg['EndDate'], cfg['SiteNameReal']
      )
conn = connectToSource()
cursor = conn.cursor()

cursor.execute(SQL,parameters)
results = cursor.fetchall()
SQLdesc = cursor.description
descCount = 0
for desc in SQLdesc:
    #print("%s %s" % (descCount,desc[0]))
    descCount = descCount + 1

referrals = {"newPlayers" : results[0][0], "welcomers" : results[1][0]}
outputObject['referrals'] = referrals
for result in results:
    print (result)

#new and old players
print ("  == New and Departed players")

SQL = """
with playerMetrics as (
    select gamertag
    , pl.playerID
    , arenaname
    , min(gametimestamp) as firstGame 
    , max(gametimestamp) as lastGame 
    from participation p 
    join players pl on p.playerID = pl.playerID
    join games g on p.gameuuid = g.gameuuid
    where arenaName ilike %s --arenaName
    group by gamerTag, pl.playerID, arenaName
),
playerMissions as (
    select playerID, count(*) as gamesPlayedInPeriod from participation p  join games g on p.gameuuid = g.gameuuid
    where gametimestamp >= %s --startDate
    and gametimestamp < %s --endDate
    group by 1
)
select 
     count (case when gamesPlayedInPeriod > 0 then 1 else null end) as totalPlayingPlayers
   , count (case when firstGame >= to_date(%s,'YYYY-MM-DD') then 1 else null end) as newPlayers
   , count (case when ((lastGame < to_date(%s,'YYYY-MM-DD') - INTERVAL '%s days' ) and lastGame >= '2019-06-01' ) then 1 else null end ) as churnedPlayers 
from playerMetrics pm1 join playerMissions pm2 on pm1.playerID = pm2.playerID


"""

parameters = (
    cfg['SiteNameReal'], cfg['StartDate'], cfg['EndDate']
    , cfg['StartDate'],cfg['EndDate'], cfg['ChurnDuration']
    )
conn = connectToSource()
cursor = conn.cursor()

cursor.execute(SQL,parameters)
results = cursor.fetchall()
SQLdesc = cursor.description
descCount = 0
for desc in SQLdesc:
    print("%s %s" % (descCount,desc[0]))
    descCount = descCount + 1

playerCounts = {'activePlayers' : results[0][0], 'newPlayers':results[0][1], 'churnedPlayers':results[0][2]}
outputObject['playerCounts'] = playerCounts

print(json.dumps(outputObject,indent=4))


filepart = "AnnualMetrics" 
if os.name == "nt":
	divider = "\\" 
elif os.name == "posix":
	divider = "/"
f = open("JSONBlobs%s%s%s.json" % (divider, cfg["ID Prefix"],filepart), "w+")
f.write(json.dumps(outputObject,indent=4))
DBG ("Annual metrics complete!",3)
