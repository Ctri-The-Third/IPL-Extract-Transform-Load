declare @targetID as varchar(15)
declare @ArenaName as varchar(50)
set @targetID = '9-6-106'
set @ArenaName = 'Funstation Ltd, Edinburgh, Scotland';

select count (*) as gamesPlayed, max(g.GameTimestamp) as mostRecentVisit, ArenaName from Participation p join Games g on p.GameUUID = g.GameUUID
where p.playerID = @targetID and ArenaName != @arenaName 
group by ArenaName
order by max(g.GameTimestamp) desc 