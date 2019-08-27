import json

from SQLconnector import connectToSource
import ConfigHelper as cfg


def executeBuildMonthlyStars():
	

	curMonth = cfg.getConfigString("StartDate")
	lastMonth  = cfg.getConfigString("LastMonthStart")
	endDate = cfg.getConfigString("EndDate")
	arenaName = cfg.getConfigString("SiteNameReal")
	SQL = '''declare @lastMonth as varChar(7)
	declare @curMonth as varChar(7)
	declare @arenaName as varChar(50)
	set @curMonth = ?
	set @lastMonth = ?
	set @arenaName = ?

	;

	with data as (
		select pl.PlayerID, pl.GamerTag, GameName, GameTimestamp, p.score, 
		ROW_NUMBER() over (partition by GameTimestamp order by GameTimestamp desc, score desc)  as rank, 
		count(p.PlayerID) over (partition by GameTimestamp order by GameTimestamp desc) as playerCount,
		convert(varchar(7),GameTimestamp,126) as GameMonth
		from Participation p join Games g on p.GameUUID = g.GameUUID 
		join Players pl on p.PlayerID = pl.PlayerID
		where g.ArenaName = @arenaName
	), 
	ranksAndCountsAndStars as (
		select PlayerID, GamerTag, count(*) as gamesPlayed, avg (convert(float,rank)) as AverageRank, avg(convert(float,playerCount)) as AveragePlayerCount, GameMonth  --average(rank) over (partition by GameTimestamp
		,avg(convert(float,playerCount)) *  (avg(convert(float,playerCount))/avg (convert(float,rank))) as AverageStarQuality
		from data
		where GameMonth in (@curMonth,@lastMonth)
		group by PlayerID, GamerTag, GameMonth
	)

	select r1.PlayerID, r1.GamerTag,
	round (r1.AverageStarQuality,2) as AverageStarQuality, 
	round (r1.AverageStarQuality * r1.gamesPlayed,2) as TotalStarQuality,
	round (r1.AveragePlayerCount,2) as AveragePlayerCount, 
	round (r1.AverageRank,2) as AverageRank, 
	r1.gamesPlayed as GamesPlayed,
	round (r2.AverageRank - r1.AverageRank,2) as changeInRank, 
	round (r1.AveragePlayerCount-r2.AveragePlayerCount,2) as changeInPlayers,
	round (r1.AverageStarQuality - r2.AverageStarQuality,2) as changeInStars
	from ranksAndCountsAndStars r1 left join ranksAndCountsAndStars r2 
	on r1.PlayerID = r2.PlayerID and r1.GameMonth != r2.GameMonth
	where r1.GameMonth = @curMonth
	order by AverageStarQuality desc


	'''
	conn = connectToSource()
	cursor = conn.cursor()

	cursor.execute(SQL,(curMonth,lastMonth,arenaName))
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
	for result in cursor.fetchall():
		print (result)
		ChangeInRank  = None
		ChangeInPlayers = None 
		ChangeInStars = None
		if result[7] is not None: ChangeInRank = "↑%s" % result[7]  if result[7] > 0 else "↓%s" % abs(result[7])
		if result[8] is not None: ChangeInPlayers = "↑%s" % result[8]  if result[8] > 0 else "↓%s" % abs(result[8])
		if result[9] is not None: ChangeInStars = "↑%s" % result[9]  if result[9] > 0 else "↓%s" % abs(result[9])

		JSON['Player'].append(
		{'Name' : result[1], 
		'StarQualityPerGame' : result[2], 
		'TotalStarQuality' : result[3],
		'AverageOpponents' : result[4], 
		'gamesPlayed' : result[6], 
		'AverageRank' : result[5], 
		'ChangeInRank' : ChangeInRank,
		'ChangeInPlayers' : ChangeInPlayers,
		'ChangeInSQPerGame' : ChangeInStars,
		})

	f = open("JSONBlobs\\StarQualityLatest.json", "w+")
	f.write(json.dumps(JSON,indent=4))
	f = open("JSONBlobs\\%sStarQuality.json" % cfg.getConfigString("ID Prefix"), "w+")
	f.write(json.dumps(JSON,indent=4))
	print ("Star Quality blobs written!")
