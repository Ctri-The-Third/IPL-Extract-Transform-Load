
with ranks as (
select GameTimestamp, GameName, Players.PlayerID, GamerTag, Score, 
	ROW_NUMBER() over (partition by GameTimestamp order by score desc) as gamePosition
from Games 
join Participation on Games.GameUUID = Participation.GameUUID
join Players on Participation.PlayerID = Players.PlayerID)

select round(avg(convert(float,gamePosition)),2)as AverageRank, count (*) as gamesPlayed , GamerTag from ranks

where GameTimestamp > CURRENT_TIMESTAMP - 28

group by GamerTag 
order by AverageRank asc

