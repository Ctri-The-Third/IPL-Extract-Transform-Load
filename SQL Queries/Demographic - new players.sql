select distinct arenaName from games 
declare @startDate as varchar(10) 
declare @endDate as varchar(10) 
declare @lastMonth as varchar(10) 
declare @targetArena as varchar(50)
set @targetArena = 'Funstation Ltd, Edinburgh, Scotland'
set @startDate = '2019-07-01'
set @endDate = '2019-08-01'
set @lastMonth = '2019-06-01';
with data as (
select count(*) missions, min(g.gameTimestamp) firstSeen, max(g.gameTimestamp) lastSeen, p.playerID, pl.GamerTag
from Participation p join Games G on p.GameUUID = g.GameUUID
join players pl on p.PlayerID = pl.PlayerID
where g.ArenaName = @targetArena
group by p.PlayerID, pl.GamerTag
)
select * from data where 
firstSeen >= @startDate and firstSeen <= @endDate
or lastSeen - 30 >@endDate