with PlayersInGame as ( --each individual game
	SELECT 
	Count (Players.GamerTag) as playersInGame, 
	Games.GameUUID as gameID
	FROM Games 
	join Participation on participation.GameUUID = Games.GameUUID
	join Players on Participation.PlayerID = Players.PlayerID
	where GameTimestamp >= '2019-06-01'
	and GameTimeStamp < '2020-01-01'
	and games.ArenaName ilike '%edinburgh%'
	group by Games.GameUUID ),
averageOpponents as --average opponents per player PER MONTH
(
	select avg(cast(playersInGame as float)) as AverageOpponents
	,  players.PlayerID 
	, to_char(GameTimestamp,'YYYY-MM') as gameMonth
	from Participation 
	join PlayersInGame on Participation.GameUUID = PlayersInGame.gameID
	join Games on Games.GameUUID = PlayersInGame.gameID
	join Players on Participation.PlayerID = players.PlayerID
	where games.ArenaName ilike '%edinburgh%'
	group by  players.PlayerID	, 3	
),
totalGamesPlayed as --total games played PER MONTH
(
	select count(*) as gamesPlayed
	, Participation.PlayerID
	, to_char(GameTimestamp,'YYYY-MM') as gameMonth
	from Participation 
	join Games on Games.GameUUID = Participation.GameUUID
	where GameTimestamp >= '2019-06-01'
	and GameTimeStamp < '2020-01-01'
	and games.ArenaName ilike '%edinburgh%'
	group by Participation.PlayerID, 3
	
),
Ranks as --each individual game
(
	select GameTimestamp
	, to_char(GameTimestamp,'YYYY-MM') as gameMonth
	, GameName, Players.PlayerID, GamerTag, Score 
	, ROW_NUMBER() over (partition by GameTimestamp order by score desc) as gamePosition
	from Games 
	join Participation on Games.GameUUID = Participation.GameUUID
	join Players on Participation.PlayerID = Players.PlayerID
	where GameTimestamp >= '2019-06-01'
	and GameTimeStamp < '2020-01-01'
	and games.ArenaName ilike '%edinburgh%'
),
AverageRanks as --average rank per player per month
( select PlayerID
	, AVG(cast(gamePosition as float)) as AverageRank
	, gameMonth 
	from Ranks
	group by PlayerID, gameMonth
), 
AverageScores as ( --average standard score per player per month
SELECT 
	Players.PlayerID, 	
	avg(Score) as averageScore,
	AverageRanks.gameMonth	
	FROM Participation
	inner join Players on Participation.PlayerID = Players.PlayerID
	inner join Games on Participation.GameUUID = Games.GameUUID
	join totalGamesPlayed on totalGamesPlayed.PlayerID = Players.PlayerID
	join averageOpponents on averageOpponents.PlayerID = Players.PlayerID
	join AverageRanks on AverageRanks.PlayerID = Players.PlayerID
	where GameTimestamp >= '2019-06-01'
	and GameTimeStamp < '2020-01-01'
	and games.ArenaName ilike '%edinburgh%'
	and (
	Games.GameName in ('Team','3 Teams','4 Teams', 'Colour Ranked','Individual')
    or Games.GameName in ('Standard - Solo', 'Standard - Team','Standard [3 Team] (10)','Standard [3 Team] (15)','Standard 2 Team',
    'Standard 3 Team','Standard 4 Team','Standard Individual','Standard Multi team','- Standard [2 Team] (15))')
	)
	group by Players.PlayerID, AverageRanks.gameMonth
 ),
StarQuality as --group by 
(
	SELECT distinct Players.PlayerID, GamerTag
	, round(cast(AverageOpponents as numeric),2) as AverageOpponents, gamesPlayed
	, round(cast(AverageRank as numeric),2) as AverageRank
	, round(cast(AverageOpponents *  1/(AverageRank/AverageOpponents) as numeric),2) as AvgQualityPerGame
	, round(cast(AverageOpponents * gamesPlayed * 1/(AverageRank/AverageOpponents) as numeric),2) as TotalQualityScore, averageScore, AchievementScore
	, averageRanks.gameMonth
	from Players
	join totalGamesPlayed 
	  on totalGamesPlayed.PlayerID = Players.PlayerID 
	join averageOpponents 
	  on averageOpponents.PlayerID = Players.PlayerID
	  and averageOpponents.gameMonth = totalGamesPlayed.gamemonth
	join AverageRanks 
	  on AverageRanks.PlayerID = Players.PlayerID
	  and averageRanks.gamemonth = averageOpponents.gamemonth
	left join AverageScores 
	  on AverageScores.PlayerID = Players.PlayerID 
	  and averageScores.gameMonth = averageRanks.gameMonth
	--group by averageRanks.gameMonth
),
GoldenTopX as 
(
	select PlayerID
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
),
BestScorer as (
	SELECT PlayerID --, GamerTag, round(AverageOpponents,2) as AverageOpponents, gamesPlayed, round(AverageRank,2) as AverageRank, 
	--round((AverageOpponents *  1/(AverageRank/AverageOpponents)),2) as AvgQualityPerGame,
	--round((AverageOpponents * gamesPlayed * 1/(AverageRank/AverageOpponents)),2) as TotalQualityScore, averageScore, AchievementScore
	from AverageScores 
	where PlayerID not in (select PlayerID from GoldenTop3) 
	order by averageScore desc
	limit 1
),
Achievers as (
    select playerID, count(*) achievements
    from PlayerAchievement pa join AllAchievements aa on aa.AchID = pa.AchID
    where achievedDate is not null and aa.ArenaName ilike '%edinburgh%'
    group by playerID 
),
BestAchiever as(

	SELECT Players.PlayerID
	--GamerTag, round(AverageOpponents,2) as AverageOpponents, gamesPlayed, round(AverageRank,2) as AverageRank, 
	--round((AverageOpponents *  1/(AverageRank/AverageOpponents)),2) as AvgQualityPerGame,
	--round((AverageOpponents * gamesPlayed * 1/(AverageRank/AverageOpponents)),2) as TotalQualityScore, averageScore, AchievementScore
	from Players
	join totalGamesPlayed on totalGamesPlayed.PlayerID = Players.PlayerID
	where players.PlayerID not in (select PlayerID from GoldenTop3) and Players.PlayerID not in (select PlayerID from BestScorer)
	order by Players.AchievementScore desc
	limit 1
)
select * from GoldenTop3 g3  join StarQuality sq on
sq.playerID = g3.playerID and 
sq.gameMonth = g3.gameMonth
order by g3.gameMonth asc, g3.playerRank asc
