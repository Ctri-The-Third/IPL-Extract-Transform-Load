/****** Thursday night participation ******/

with data as (
select GameTimestamp, GameName, Players.PlayerID, GamerTag, Score, 
	ROW_NUMBER() over (partition by GameTimestamp order by score desc) as gamePosition,
	count (convert(datetime,GameTimestamp,23)) over (partition by GamerTag) as GamesNightGamesPlayed
	
	from Games 
	join Participation on Games.GameUUID = Participation.GameUUID
	join Players on Participation.PlayerID = Players.PlayerID
	
	and CONVERT(int,GameTimestamp) % 7 = 4  --Thursdays
	
	--and convert(dateTime,GameTimestamp,8) > '19:50:00'
	--and convert(dateTime,GameTimestamp,8) < '21:10:00'

),roster as (
select (CONVERT(int, CURRENT_TIMESTAMP) - CONVERT(int, Max(GameTimestamp))) /7   as recency, PlayerID, GamerTag from data 
group by PlayerID, GamerTag)

select * from roster 
where recency < 56
order by recency asc


