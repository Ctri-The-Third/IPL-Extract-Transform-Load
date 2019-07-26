with data as (
	select GamerTag, GameTimestamp, GameName, Score, insertedTimestamp
	from Participation p
	join players pl on p.PlayerID = pl.PlayerID
	join games g on g.GameUUID = p.GameUUID 
)
select * from data 
order by GameTimestamp desc