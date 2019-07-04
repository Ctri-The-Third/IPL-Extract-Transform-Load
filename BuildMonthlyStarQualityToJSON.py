import json

from SQLconnector import connectToSource
from ConfigHelper import getConfig

config = getConfig()

startDate = config["StartDate"]
endDate = config["EndDate"]
SQL = '''DECLARE @startDate as date
DECLARE @endDate as date;
SET @startDate = ?;
SET @endDate = ?;

with PlayersInGame as (
	SELECT 
	Count (Players.GamerTag) as playersInGame, 
	Games.GameUUID as gameID
	FROM [LaserScraper].[dbo].[Games] as Games
	join Participation on participation.GameUUID = Games.GameUUID
	join Players on Participation.PlayerID = Players.PlayerID
	where GameTimestamp >= @startDate
	and GameTimeStamp < @endDate
	group by Games.GameUUID ),
averageOpponents as 
(
	select avg(cast(playersInGame as float)) as AverageOpponents,  players.PlayerID from Participation 
	join PlayersInGame on Participation.GameUUID = PlayersInGame.gameID
	join Games on Games.GameUUID = PlayersInGame.gameID
	join Players on Participation.PlayerID = players.PlayerID
	group by  players.PlayerID
		
),
totalGamesPlayed as 
(
	select count(*) as gamesPlayed,  Participation.PlayerID
	from Participation 
	join Games on Games.GameUUID = Participation.GameUUID
	where GameTimestamp >= @startDate
	and GameTimeStamp < @endDate
	group by Participation.PlayerID
),
Ranks as 
(
	select GameTimestamp, GameName, Players.PlayerID, GamerTag, Score, 
		ROW_NUMBER() over (partition by GameTimestamp order by score desc) as gamePosition
	from Games 
	join Participation on Games.GameUUID = Participation.GameUUID
	join Players on Participation.PlayerID = Players.PlayerID
	where GameTimestamp >= @startDate
	and GameTimestamp < @endDate
),
AverageRanks as 
( select PlayerID, AVG(CONVERT(float,gamePosition)) as AverageRank from Ranks
	group by PlayerID)



SELECT Players.PlayerID, GamerTag, round(AverageOpponents,2) as AverageOpponents, gamesPlayed, round(AverageRank,2) as AverageRank, 
round((AverageOpponents *  1/(AverageRank/AverageOpponents)),2) as AvgQualityPerGame,
round((AverageOpponents * gamesPlayed * 1/(AverageRank/AverageOpponents)),2) as TotalQualityScore from Players
join totalGamesPlayed on totalGamesPlayed.PlayerID = Players.PlayerID
join averageOpponents on averageOpponents.PlayerID = Players.PlayerID
join AverageRanks on AverageRanks.PlayerID = Players.PlayerID
order by AvgQualityPerGame desc

'''
conn = connectToSource()
cursor = conn.cursor()

cursor.execute(SQL,(startDate,endDate))
JSON = {
    'ScoreTitle' : "Star Quality for all known players, between {0} and {1}" .format(startDate,endDate),
    'ScoreGreaterOrEqualDate' : startDate,
    'ScoreLessDate' : endDate,
    'Player' : [{
    #    'Name' : "C'tri",
    #    'AverageScore' : -1,
    #    'MissionsPlayed' : -1,
    }],
    }
for result in cursor.fetchall():
    print (result)
    JSON['Player'].append({'Name' : result[1], 'AverageOpponents' : result[2], 'gamesPlayed' : result[3], 'AverageRank' : result[4], 'StarQualityPerGame' : result[5], 'TotalStarQuality' : result[6]})

f = open("JSONBlobs\\StarQualityLatest.json", "w+")
f.write(json.dumps(JSON))
f = open("JSONBlobs\\StarQuality{0}to{1}.json".format(startDate,endDate), "w+")
f.write(json.dumps(JSON))
print ("Star Quality blobs written!")