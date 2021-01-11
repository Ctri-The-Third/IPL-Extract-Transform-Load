/****** Thursday night participation ******/
--incomplete. Needs more accurate filtering to stop games that creep in from earlier / later in the night.
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

/*select * from data 
where GameTimestamp > '2019-06-06'
and GameTimestamp < '2019-06-07'
order by GameTimestamp desc, gamePosition asc*/

select max(GamesNightGamesPlayed) as GamesNightGamesPlayed, round(avg(convert(float,gamePosition)),2) as averageRank, PlayerID,GamerTag from data 
where GamesNightGamesPlayed > 3 
group by PlayerID, GamerTag
order by averageRank asc
/**/

