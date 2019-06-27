/*** break down player quality by game **/

/*SELECT Players.PlayerID, GamerTag, round(AverageOpponents,2) as AverageOpponents, gamesPlayed, round(AverageRank,2) as AverageRank, 
round((AverageOpponents *  1/(AverageRank/AverageOpponents)),2) as AvgQualityPerGame,
round((AverageOpponents * gamesPlayed * 1/(AverageRank/AverageOpponents)),2) as TotalQualityScore from Players
*/

DECLARE @targetID  as varchar (20) 
set @targetID = '7-9-126';

with Ranks as 
(
	select GameTimestamp,games.GameUUID, GameName, Players.PlayerID, GamerTag, Score, 
		ROW_NUMBER() over (partition by GameTimestamp order by score desc) as gamePosition
	from Games 
	join Participation on Games.GameUUID = Participation.GameUUID
	join Players on Participation.PlayerID = Players.PlayerID
),
totalPlayersPerGame as 
(
	select g.GameUUID, count(*) as playerCount
	from Participation p join Games g on p.GameUUID = g.GameUUID
	group by g.GameUUID
)

select ranks.GameUUID,GameTimestamp,GameName,PlayerID,GamerTag,gamePosition,playerCount, playerCount * (gamePosition / playerCount) as SQ
from ranks join totalPlayersPerGame tppg 
on ranks.GameUUID = tppg.GameUUID
where PlayerID = @targetID
order by GameTimestamp desc

