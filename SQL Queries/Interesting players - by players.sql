select distinct ArenaName from games
    declare @startDate as date
    declare @period as int
	declare @targetArena as varchar(50)
    set @startDate = '2019-08-22'
    set @period = 60
	set @targetArena = 'Laserforce Peterborough';

	with MostRecentPerArena as 
	
	(select max(g.GameTimestamp) as mostRecent, p.playerID, missions, level
	from Games g join Participation p on g.GameUUID = p.GameUUID 
	join players pl on p.PlayerID = pl.playerID 
	where ArenaName = @targetArena
	group by p.PlayerID,Missions,level)

    select  Missions, Level, PlayerID, MostRecent from MostRecentPerArena
    where mostRecent > DATEADD(day, -@period, @startDate)
    order by Missions desc, mostRecent Asc

