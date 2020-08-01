declare @startDate as date;
declare @endDate as date;
declare @targetID as varchar(20);
set @startDate = '2019-06-01';
set @endDate = '2019-07-01';
set @targetID = '9-6-106';



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