declare @TargetID as varchar (20)
SET @TargetID = '7-9-3242';
declare @TotalGamesPlayed as float


select @TotalGamesPlayed = count(*)
from Participation where PlayerID = @TargetID
group by PlayerID;


with data as ( 
	select GameUUID from Players pl
	join Participation pa on pl.PlayerID = pa.PlayerID
	where pl.PlayerID = @TargetID )

select GamerTag, p.PlayerID, count ( GamerTag) gamesPlayedTogether, count ( GamerTag) / @TotalGamesPlayed
from Participation pa 
inner join data d on pa.GameUUID = d.GameUUID
join Players p on pa.PlayerID = p.PlayerID

group by GamerTag, p.PlayerID
order by gamesPlayedTogether desc



