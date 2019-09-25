DECLARE @targetID as varchar(20)
DECLARE @startDate as Date
DECLARE @endDate as Date

SET @targetID = '9-6-106'
SET @startDate = '2019-06-01'
SET @endDate = '2019-07-01';

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

	select * from Vanquished