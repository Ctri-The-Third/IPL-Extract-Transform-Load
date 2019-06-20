/****** Thursday night participation ******/

with data as (
select GameTimestamp, GameName, Players.PlayerID, GamerTag, Score, 
	ROW_NUMBER() over (partition by GameTimestamp order by score desc) as gamePosition,
	count (convert(datetime,GameTimestamp,23)) over (partition by GamerTag) as GamesNightGamesPlayed
	
	from Games 
	join Participation on Games.GameUUID = Participation.GameUUID
	join Players on Participation.PlayerID = Players.PlayerID
	where GameTimestamp > '2019-05-23'
	--and convert(dateTime,GameTimestamp,8) > '19:50:00'
	--and convert(dateTime,GameTimestamp,8) < '20:10:00'
	and CONVERT(int,GameTimestamp) % 7 = 4  --Thursdays
)
select max(GamesNightGamesPlayed) as GamesNightGamesPlayed, round(avg(convert(float,gamePosition)),2) as averageRank, PlayerID,GamerTag from data 
--where CONVERT(int,GameTimestamp) % 7 = 3  --Thursdays
group by PlayerID, GamerTag
order by averageRank asc


