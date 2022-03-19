import json
import os
from SQLconnector import connectToSource
import ConfigHelper as cfg
from DBG import DBG

def executeBuildMonthlyStars():
	cachedconfig = cfg.getConfig()	

	curMonth = cachedconfig["StartDate"][0:7]
	lastMonth  = cachedconfig["LastMonthStart"][0:7]
	endDate = cachedconfig["EndDate"]
	arenaName = cachedconfig["SiteNameReal"]
	SQL = '''
with subsetOfData as 
(
	select playerID
	, gamerTag
	, gamemonth
	, avg(playercount) as AveragePlayerCount
	, count(*) as GamesPlayed
	, avg(Starsforgame) as AverageStarQuality
	, sum(Starsforgame) as TotalStarQuality
	, avg(rank) as AverageRank 
	from public."participationWithStars"
	where arenaName = %s --
	and GameMonth in (%s,%s) --	
	group by 1,2,3
)

select r1.PlayerID, r1.GamerTag,
round (cast(r1.AverageStarQuality as numeric),2) as AverageStarQuality, 
round (cast(r1.AverageStarQuality * r1.gamesPlayed as numeric),2) as TotalStarQuality,
round (cast(r1.AveragePlayerCount as numeric),2) as AveragePlayerCount, 
round (cast(r1.AverageRank as numeric),2) as AverageRank, 
r1.gamesPlayed as GamesPlayed,
round (cast(r2.AverageRank - r1.AverageRank as numeric),2) as changeInRank, 
round (cast(r1.AveragePlayerCount-r2.AveragePlayerCount as numeric),2) as changeInPlayers,
round (cast(r1.AverageStarQuality - r2.AverageStarQuality as numeric),2) as changeInStars
from subsetOfData r1 left join subsetOfData  r2 
on r1.PlayerID = r2.PlayerID and r1.GameMonth != r2.GameMonth
where r1.GameMonth = %s --
order by AverageStarQuality desc
	'''

	conn = connectToSource()
	cursor = conn.cursor()

	cursor.execute(SQL,(arenaName,curMonth,lastMonth,curMonth))
	JSON = {
		'ScoreTitle' : "Star Quality for all known players, between {1} and {0}" .format(curMonth,lastMonth),
		'ScoreGreaterOrEqualDate' : curMonth,
		'ScoreLessDate' : lastMonth,
		'Player' : [{
		#    'Name' : "C'tri",
		#    'AverageScore' : -1,
		#    'MissionsPlayed' : -1,
		}],
		}
	breakdownSQL = """
		with data as (
			select pl.PlayerID, pl.GamerTag, GameName, GameTimestamp, p.score, 
			ROW_NUMBER() over (partition by GameTimestamp order by GameTimestamp desc, score desc)  as rank, 
			count(p.PlayerID) over (partition by GameTimestamp order by GameTimestamp desc) as playerCount,
			TO_CHAR(GameTimestamp,'YYYY-MM') as GameMonth
			from Participation p join Games g on p.GameUUID = g.GameUUID 
			join Players pl on p.PlayerID = pl.PlayerID
			where g.ArenaName = %s
		)
		select gamename, rank, playerCount 
		, round(cast((cast(playerCount as float) * cast(playerCount as float)) / cast(rank as float) as numeric),2) as stars
		from data 
		where GameMonth = %s
		and playerID ilike %s
		order by gametimestamp desc 
	"""
	SQResults = cursor.fetchall()
	counter = 0 
	for result in SQResults:
		#print (result)
		ChangeInRank  = None
		ChangeInPlayers = None 
		ChangeInStars = None
		if result[7] is not None: ChangeInRank = "↑%s" % result[7]  if result[7] > 0 else "↓%s" % abs(result[7])
		if result[8] is not None: ChangeInPlayers = "↑%s" % result[8]  if result[8] > 0 else "↓%s" % abs(result[8])
		if result[9] is not None: ChangeInStars = "↑%s" % result[9]  if result[9] > 0 else "↓%s" % abs(result[9])

		SQObject = {
		'JSID' : counter, 
		'Name' : result[1], 
		'StarQualityPerGame' : "%s" % result[2], 
		'TotalStarQuality' : "%s" % result[3],
		'AverageOpponents' : "%s" % result[4], 
		'gamesPlayed' : result[6], 
		'AverageRank' : "%s" % result[5], 
		'ChangeInRank' : ChangeInRank,
		'ChangeInPlayers' : ChangeInPlayers,
		'ChangeInSQPerGame' : ChangeInStars,
		'breakdown' : []
		}

		cursor.execute(breakdownSQL,(arenaName,curMonth,result[0]))
		breakdownResults = cursor.fetchall()
		for breakdownEntry in breakdownResults:
			SQBreakdown = {
			"gameName":breakdownEntry[0],
			"rank":breakdownEntry[1],
			"totalPlayers" : breakdownEntry[2],
			"starsForGame" : "%s" % breakdownEntry[3]
			}
			SQObject['breakdown'].append(SQBreakdown)

		JSON['Player'].append(SQObject)
		counter = counter + 1

	filepart = "StarQuality" 
	if os.name == "nt":
		divider = "\\" 
	elif os.name == "posix":
   		divider = "/"
	f = open("JSONBlobs%s%s%s.json" % (divider, cfg.getConfigString("ID Prefix"),filepart), "w+")
	f.write(json.dumps(JSON,indent=4))
	DBG ("Star Quality blobs written!",3)
