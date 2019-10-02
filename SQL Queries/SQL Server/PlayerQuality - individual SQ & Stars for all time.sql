/*** break down player quality by game **/

/*SELECT Players.PlayerID, GamerTag, round(AverageOpponents,2) as AverageOpponents, gamesPlayed, round(AverageRank,2) as AverageRank, 
round((AverageOpponents *  1/(AverageRank/AverageOpponents)),2) as AvgQualityPerGame,
round((AverageOpponents * gamesPlayed * 1/(AverageRank/AverageOpponents)),2) as TotalQualityScore from Players
*/

DECLARE @targetID  as varchar (20) 
DECLARE @ArenaName as varchar(50)
set @targetID = '7-9-220040';
set @ArenaName = 'Funstation Ltd, Edinburgh, Scotland';

with Ranks as 
(
	select GameTimestamp,games.GameUUID, GameName, Players.PlayerID, GamerTag, Score, 
		ROW_NUMBER() over (partition by GameTimestamp order by score desc) as gamePosition
	from Games 
	join Participation on Games.GameUUID = Participation.GameUUID
	join Players on Participation.PlayerID = Players.PlayerID
	where Games.ArenaName = @ArenaName
),
totalPlayersPerGame as 
(
	select g.GameUUID, count(*) as playerCount
	from Participation p join Games g on p.GameUUID = g.GameUUID
	group by g.GameUUID
)
, starData0 as  (
select concat(concat(DATEPART(yyyy,GameTimestamp),'-'),CONCAT (CASE WHEN DATEPART(MM,Gametimestamp) < 10 THEN '0' END ,DATEPART(MM,Gametimestamp))) as month, ranks.GameUUID,GameTimestamp,GameName,PlayerID,GamerTag,gamePosition,playerCount, playerCount  * ( playerCount  / gamePosition ) as SQ
from ranks join totalPlayersPerGame tppg 
on ranks.GameUUID = tppg.GameUUID
--where PlayerID = @targetID

)
,starData1 as (
select month, PlayerID,count(*) games,round(avg(cast(gamePosition as float)),2) avgRank, round(avg(cast(playercount as float)),2) avgOpponents, round(avg(cast(SQ as float)),2) avgSQ
from starData0 
group by  month, PlayerID
)
, starData2 as (
select ROW_NUMBER() over (partition by month order by month desc, avgSQ desc) SQrank, * from starData1)

, StdData0 as( select 
	p.PlayerID, 
	GamerTag, 
	avg(Score) as averageScore,
	count(GamerTag) as gamesPlayed,
	convert(varchar(7),GameTimestamp,126) as GameMonth
	
  FROM Participation p
  inner join Players pl on p.PlayerID = pl.PlayerID
  inner join Games g on p.GameUUID = g.GameUUID
  --where convert(varchar(7),GameTimestamp,126) in (@curMonth,@lastMonth)
  and (g.GameName in ('Team','3 Teams','4 Teams', 'Colour Ranked','Individual') or
   g.GameName in ('Continous Ind','Standard 2 Team','Standard 3 Team','Standard 4 Team','Standard Individual','Standard Multi team' )
  )
  and g.ArenaName = @ArenaName
  GROUP BY p.PlayerID, pl.GamerTag, convert(varchar(7),GameTimestamp,126)
)
 , stdData1 as (
 select *, ROW_NUMBER() over (partition by GameMonth order by averageScore desc) as stdRank from StdData0
 )
 
select top (5) month,SQrank,avgSQ,games,stdRank,averageScore,gamesPlayed
from starData2 sq
join StdData1 sd on sq.PlayerID = sd.PlayerID and sq.month = sd.GameMonth
where sq.PlayerID = @targetID 



