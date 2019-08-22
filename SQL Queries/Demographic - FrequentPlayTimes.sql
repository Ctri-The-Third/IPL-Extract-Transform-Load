declare @targetID as varchar(50)
declare @arenaName as varchar(50)
set @targetID = '9-6-106';
set @arenaName = 'Funstation Ltd, Edinburgh, Scotland';



with dateData as (
select distinct case 
	when DATEPART( dw, GameTimestamp) = 1 then 'Sunday'
	when DATEPART( dw, GameTimestamp) = 2 then 'Monday'
	when DATEPART( dw, GameTimestamp) = 3 then 'Tuesday'
	when DATEPART( dw, GameTimestamp) = 4 then 'Wednesday'
	when DATEPART( dw, GameTimestamp) = 5 then 'Thursday'
	when DATEPART( dw, GameTimestamp) = 6 then 'Friday'
	when DATEPART( dw, GameTimestamp) = 7 then 'Saturday'
end as dayName, 
	DATEPART (dw,GameTimestamp) as day
from Games
),
data as (
	select count (*) as games, DATEPART( dw, GameTimestamp) as day, datePart(HH,GameTimestamp) as hour
	from players pl join Participation p on pl.PlayerID = p.PlayerID 
	join games g on p.GameUUID = g.GameUUID
	where p.playerID = @targetID
	and g.ArenaName = @arenaName
	group by DATEPART( dw, GameTimestamp), datePart(HH,GameTimestamp)
)

select top (3) games,dayName,hour from data d join   dateData dd on d.day =dd.day
order by games desc
