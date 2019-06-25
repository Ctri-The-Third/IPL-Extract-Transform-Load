import requests
import json
import importlib

from SQLconnector import connectToSource
targetID = '9-6-106'
startDate = '2019-06-01'
endDate = '2019-07-01'

infoQuery = """declare @startDate as date;
declare @endDate as date;
declare @targetID as varchar(20);
set @startDate = ?;
set @endDate = ?;
set @targetID = ?;



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
	and GameTimeStamp < @endDate
),
AverageRanks as 
( select PlayerID, AVG(CONVERT(float,gamePosition)) as AverageRank from Ranks
	group by PlayerID),

totalAchievements as  (
select  sum ( case when achievedDate is null then 0 when achievedDate is not null then 1 end) as AchievementsCompleted, PlayerID from PlayerAchievement
group by PlayerID
)



select Players.PlayerID, GamerTag,players.Level, Missions, round(AverageOpponents,2) as AverageOpponents, gamesPlayed, round(AverageRank,2) as AverageRank, 
round((AverageOpponents *  1/(AverageRank/AverageOpponents)),2) as AvgQualityPerGame,
round((AverageOpponents * gamesPlayed * 1/(AverageRank/AverageOpponents)),2) as TotalQualityScore,
totalAchievements.AchievementsCompleted, totalAchievements.PlayerID as TaPID
from Players 
join totalGamesPlayed on totalGamesPlayed.PlayerID = Players.PlayerID
join averageOpponents on averageOpponents.PlayerID = Players.PlayerID
join AverageRanks on AverageRanks.PlayerID = Players.PlayerID
join totalAchievements on totalAchievements.PlayerID = Players.PlayerID

where Players.playerID = @targetID
"""


goldenGameQuery = """DECLARE @targetID as varchar(20)
DECLARE @startDate as date
DECLARE @endDate as date

SET @targetID = ?
SET @startDate = ?
SET @endDate = ?;

with PlayersInGame as (
	SELECT 
	Count (Players.GamerTag) as playersInGame, 
	Games.GameUUID as gameID
	FROM [LaserScraper].[dbo].[Games] as Games
	join Participation on participation.GameUUID = Games.GameUUID
	join Players on Participation.PlayerID = Players.PlayerID

	group by Games.GameUUID ),

Ranks as 
(
	select GameTimestamp, GameName, Players.PlayerID, GamerTag, Score, Games.GameUUID, 
		ROW_NUMBER() over (partition by GameTimestamp order by score desc) as gamePosition
	from Games 
	join Participation on Games.GameUUID = Participation.GameUUID
	join Players on Participation.PlayerID = Players.PlayerID
),
GoldenGame as (


	select  top (1) r.Score, r.GamerTag,r.GameUUID, GameName, r.PlayerID, gamePosition, playersInGame, GameTimestamp
	,round((playersInGame *  (playersInGame/gamePosition)),2) as StarQuality
	from Ranks r join PlayersInGame pig on r.GameUUID = pig.gameID
	where PlayerID = @targetID
	and GameTimestamp >= @startDate
	and GameTimeStamp < @endDate
	order by StarQuality desc, score desc 
	
	),
Vanquished as (
	select g.PlayerID, g.GameTimestamp, g.gamePosition victoryPos,  g.GamerTag victorName, g.Score victorScore, g.GameName, g.StarQuality victorStarQuality, r.PlayerID vanquishedID, r.GamerTag vanquishedName ,r.gamePosition as vanquishedPos  from 
	Ranks r inner join GoldenGame g on r.gameUUID = g.GameUUID
	where g.PlayerID != r.PlayerID
	and g.gamePosition < r.gamePosition


)

	select * from Vanquished"""

goldenAchievementQuery = """DECLARE @TargetID as Varchar(10)
SET @TargetID = ? ;


with firstEarned as (
select distinct min (achievedDate) over (partition by Image) as firstAchieved, Image
from PlayerAchievement
where achievedDate is not null

),
data as ( select count(*) playersEarned,  pa.image, achName from PlayerAchievement pa join AllAchievements aa on pa.Image = aa.image
where achievedDate is not null
group by AchName, pa.Image) 

select top(10) PlayerID, data.AchName, Description, fe.firstAchieved, playersEarned from PlayerAchievement pa 
join data on data.Image = pa.Image
join firstEarned fe on fe.Image = data.Image
join AllAchievements aa on pa.Image = aa.image
where PlayerID = @TargetID
order by playersEarned asc, firstAchieved asc
"""

conn = connectToSource()
cursor = conn.cursor()

result = cursor.execute(infoQuery,(startDate,endDate,targetID))
row = result.fetchone()
print(row)
print ("Players.PlayerID, GamerTag, round(AverageOpponents,2) as AverageOpponents, gamesPlayed,  AverageRank")
SkillLevelName = ["Recruit","Gunner","Trooper","Captain","Star Lord","Laser Master"]

JSONobject = {}
JSONobject["PlayerName"] = row[1]
JSONobject["HomeArenaTrunc"] = "Laserstation Edinburgh"
JSONobject["SkillLevelName"] = SkillLevelName[row[2]]
JSONobject["MonthlyGamesPlayed"] = row[5]
JSONobject["AllGamesPlayed"] = row[3]
JSONobject["StarQuality"] = row[7]
JSONobject["Achievements"] = row[9]

result = cursor.execute(goldenGameQuery,(targetID,startDate,endDate))
rows = result.fetchall()
row = rows[0]
print(row)
print ("g.PlayerID, g.GameTimestamp, victoryPos,   victorName,  victorScore, g.GameName, victorStarQuality,  vanquishedID, vanquishedName , vanquishedPos")
ordinalranks = ["0th","1st","2nd","3rd","4th","5th","6th","7th","8th","9th","10th"]
JSONobject["GGName"] = row[5]
JSONobject["GGRank"] = ordinalranks[row[2]]
JSONobject["GGStars"] = "%i stars" % row[6]
JSONobject["GGVanq1"] = rows[0][8]
JSONobject["GGVanq2"] = rows[1][8]
JSONobject["GGVanq3"] = rows[2][8]
JSONobject["GGVanq4"] = '%i others' % (len(rows) - 3)

result = cursor.execute(goldenAchievementQuery,(targetID))
row = result.fetchone()
print (row)
JSONobject["GAName"] = row[1]
JSONobject["GADesc"] = row[2]

ordinalOthers = ["No one else has","Only one other person has","Only two others have","Only %i others have" % row[4]]

JSONobject["GAOthers"] = ordinalOthers[min(row[4],3)]


f = open("JSONBlobs\\playerBlob.json", "w+")
f.write(json.dumps(JSONobject))
print ("Player profile blobs written!")