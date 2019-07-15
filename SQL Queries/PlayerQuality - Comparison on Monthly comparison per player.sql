declare @lastMonth as varChar(7)
declare @curMonth as varChar(7)
set @lastMonth = '2019-06'
set @curMonth = '2019-07'
;

with data as (
	select pl.PlayerID, pl.GamerTag, GameName, GameTimestamp, p.score, 
	ROW_NUMBER() over (partition by GameTimestamp order by GameTimestamp desc, score desc)  as rank, 
	count(p.PlayerID) over (partition by GameTimestamp order by GameTimestamp desc) as playerCount,
	convert(varchar(7),GameTimestamp,126) as GameMonth
	from Participation p join Games g on p.GameUUID = g.GameUUID 
	join Players pl on p.PlayerID = pl.PlayerID
	where convert(varchar(7),GameTimestamp,126) in (@curMonth,@lastMonth)
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
, r2.AverageRank
from ranksAndCountsAndStars r1 left join ranksAndCountsAndStars r2 
on r1.PlayerID = r2.PlayerID and r1.GameMonth != r2.GameMonth
where r1.GameMonth = @curMonth and r1.gamesPlayed >= 3 
order by AverageStarQuality desc