from SQLconnector import connectToSource
import ConfigHelper
import json
import os
from DBG import DBG
 

def executeBuild():
    DBG("Building arena metrics",3)
    conn = connectToSource()
    cursor = conn.cursor()

    outputObject = {}

    cfg = ConfigHelper.getConfig()
    startYear = int(cfg["StartDate"][0:4])
    endYear = startYear + 1
    startYear = "%s-01-01" % startYear
    endYear = "%s-01-01" % endYear



    #topGames
    #print ("  == Which games were played")

    SQL = """
with gamesbyname as (
select count(*) as gameCount, gamename from games g 
    where arenaName ilike %s
    and gametimestamp >= %s
    and gametimestamp < %s
    group by 2
    order by 1 desc
),
totalGames as (
	select sum(gameCount) totalGames
	from gamesbyname
)
select cast(gamecount as integer), gamename from gamesbyname full outer join totalgames on true 
where (gamecount / totalgames) > 0.01
union 
select cast(sum(gamecount) as integer), 'other' from gamesbyname full outer join totalgames on true 
where (gamecount / totalgames) <= 0.01
order by 1 desc; 

    """

    parameters = (
        cfg['SiteNameReal'], startYear, endYear
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
        #print (result)
        game = {'gameName' : result[1], 'timesPlayed' : result[0] }
        gamesPlayed.append(game)
    outputObject['gamesPlayed'] = gamesPlayed
    #referrals
    #print ("  == Referrals and Welcomers")

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
        startYear, endYear, cfg['SiteNameReal']
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

    #new and old players
    #print ("  == New and Departed players")

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
    , count (case when ((lastGame < to_date(%s,'YYYY-MM-DD') - INTERVAL '%s days' ) and lastGame >= %s ) then 1 else null end ) as churnedPlayers 
    from playerMetrics pm1 join playerMissions pm2 on pm1.playerID = pm2.playerID
    """

 
    parameters = (
        cfg['SiteNameReal'], startYear, endYear
        , startYear,endYear, cfg['ChurnDuration'], startYear
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

    playerCounts = {'activePlayers' : results[0][0], 'newPlayers':results[0][1], 'churnedPlayers':results[0][2]}
    outputObject['playerCounts'] = playerCounts

    #print(json.dumps(outputObject,indent=4))
        
    #MEMBER PERCENTILES - visits
    SQL = """with data as (select 
percent_rank() over (order by count(distinct date_trunc('day',g.gametimestamp))) as percentile
,count(distinct date_trunc('day',g.gametimestamp)) as visits
, pl.playerID from players pl join participation p on pl.playerID = p.playerID
join games g on g.gameuuid = p.gameuuid
where g.arenaname ilike %s
and g.gametimestamp >= %s
and g.gametimestamp < %s
group by pl.playerID
),
finalresults as (
	select
	count (case when visits >= 1 and visits < 2 then 1 else null end) as one,
	count (case when visits >= 2 and visits < 3 then 1 else null end) as twoVisits,
	count (case when visits >= 3 and visits < 5 then 1 else null end) as LessThanFive,
	count (case when visits >= 5 and visits < 11 then 1 else null end) as LessThanEleven, 
	count (case when visits >= 11 then 1 else null end) as MoreThanEleven
	from data 
)
select * from finalResults

"""
    parameters = [cfg['SiteNameReal'], startYear, endYear]
    cursor.execute(SQL,parameters)
    result = cursor.fetchone()
    
    
    visits = [
        {"caption":"1 visit", "players":result[0]}
        , {"caption":"2 visits", "players": result[1]}
        , {"caption":"3-4 visits", "players": result[2]}
        , {"caption":"5-10 visits", "players": result[3]}
        , {"caption":"11+ visits", "players": result[4]}
    ]
        
    
    outputObject['regularsAggregateVisits'] = visits
    #referrals
    #print ("  == Referrals and Welcomers")

    #MEMBER PERCENTILES - GAMES
    SQL = """with data as (select 
percent_rank() over (order by count(distinct date_trunc('day',g.gametimestamp))) as percentile
,count(distinct date_trunc('day',g.gametimestamp)) as visits
, pl.playerID from players pl join participation p on pl.playerID = p.playerID
join games g on g.gameuuid = p.gameuuid
where g.arenaname ilike %s
and g.gametimestamp >= %s
and g.gametimestamp < %s
group by pl.playerID
),
finalresults as (
	select
	count (case when visits >= 1 and visits < 3 then 1 else null end) as max2,
	count (case when visits >= 3 and visits < 7 then 1 else null end) as max6,
	count (case when visits >= 7 and visits < 13 then 1 else null end) as max12,
	count (case when visits >= 13 and visits < 36 then 1 else null end) as max35, 
	count (case when visits >= 36 then 1 else null end) as min36
	from data 
)
select * from finalResults"""

    parameters = [cfg['SiteNameReal'], startYear, endYear]
    cursor.execute(SQL,parameters)
    result = cursor.fetchone()
    
    
    games = [
        {"caption":"1-2 games", "players":result[0]}
        , {"caption":"3-6 games", "players": result[1]}
        , {"caption":"7-12 games", "players": result[2]}
        , {"caption":"13-35 games", "players": result[3]}
        , {"caption":"36+ games", "players": result[4]}
    ]
    outputObject['regularsAggregateGames'] = games

    #MEMBER PERCENTILES - RETENTION
    SQL = """with preData as 
(select  p.playerid
, min(g.gametimestamp) as firstSeen
, max(g.gametimestamp) as lastSeen
, floor(extract(epoch from max(g.gametimestamp) - min(g.gametimestamp))/604800)::int as weeks
from games g  join participation p on p.gameuuid = g.gameuuid
where arenaname ilike %s
and g.gametimestamp < %s

group by 1 
),
data as 
(select * from preData where lastSeen >= %s
),
finalresults as (
	select count(case when weeks >= 0 and weeks <= 4 then 1 else null end) as max4
	, count(case when weeks > 4 and weeks <= 12 then 1 else null end) as max12
	, count(case when weeks > 12 and weeks <= 52 then 1 else null end) as max52
	, count(case when weeks > 52 and weeks <= 104 then 1 else null end) as max104
	, count(case when weeks > 104 and weeks <= 156 then 1 else null end) as max156
	, count(case when weeks > 156  then 1 else null end) as min157
	from data
)
select * from finalresults"""
    parameters = [cfg['SiteNameReal'], endYear, startYear]

    cursor.execute(SQL,parameters)
    result = cursor.fetchone()
    
    
    retention = [
        {"caption":"0-4 weeks", "players":result[0]}
        , {"caption":"5-12 weeks", "players": result[1]}
        , {"caption":"13-52 weeks", "players": result[2]}
        , {"caption":"1-2 years", "players": result[3]}
        , {"caption":"3-4 years", "players": result[4]}
        , {"caption":"5+ years", "players": result[5]}
    ]
    outputObject['regularsAggregateRetention'] = retention

    filepart = "AnnualMetrics" 
    if os.name == "nt":
        divider = "\\" 
    elif os.name == "posix":
        divider = "/"
    f = open("JSONBlobs%s%s%s-%s.json" % (divider, cfg["ID Prefix"],filepart,startYear[0:4]), "w+")
    f.write(json.dumps(outputObject,indent=4))
    DBG ("Annual metrics complete!",3)
