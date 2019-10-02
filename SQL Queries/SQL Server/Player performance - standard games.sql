/****** Player Growth ******/

with ranks as (
	select GameTimestamp, GameName, Players.PlayerID, GamerTag, Score, 
		ROW_NUMBER() over (partition by GameTimestamp order by score desc) as gamePosition
	from Games 
	join Participation on Games.GameUUID = Participation.GameUUID
	join Players on Participation.PlayerID = Players.PlayerID
), totalPlayers as (

	select count (*) memberPlayers, gameTimestamp from
	Participation
	join Games on Games.GameUUID = Participation.GameUUID
	group by GameTimestamp
)


select GamerTag, ranks.GameTimestamp, GameName, score, memberPlayers, gamePosition, score / memberPlayers as scorePerPlayer
from ranks join totalPlayers on ranks.GameTimestamp = totalPlayers.GameTimestamp

where GamerTag like 'Rayth'
--and GameName in ('2 Teams','3 Teams','4 Teams', 'Colour Ranked','Individual')
--and (CONVERT(int,ranks.GameTimestamp) % 7 = 4  --Thursdays 
--OR CONVERT(int,ranks.GameTimestamp) % 7 = 3) --Wednesdays
order by GameTimestamp asc


