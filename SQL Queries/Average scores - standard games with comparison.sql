/****** Script for SelectTopNRows command from SSMS  ******/
declare @curMonth as varchar(7)
declare @lastMonth as varchar(7)
declare @currentArena as varchar(50)
set @curMonth = '2019-08-01'
set @lastMonth = '2019-07-01';
set @currentArena = 'Laserforce Peterborough';

with data as  ( select 
	p.PlayerID, 
	GamerTag, 
	avg(Score) as averageScore,
	count(GamerTag) as gamesPlayed,
	convert(varchar(7),GameTimestamp,126) as GameMonth
	
  FROM Participation p
  inner join Players pl on p.PlayerID = pl.PlayerID
  inner join Games g on p.GameUUID = g.GameUUID
  where convert(varchar(7),GameTimestamp,126) in (@curMonth,@lastMonth)
  and (--g.GameName in ('Team','3 Teams','4 Teams', 'Colour Ranked','Individual') or
   g.GameName in ('Continous Ind','Standard 2 Team','Standard 3 Team','Standard 4 Team','Standard Individual','Standard Multi team' ) or 1 = 1 
  )
 -- and g.ArenaName like '%@currentArena%'
  GROUP BY p.PlayerID, pl.GamerTag, convert(varchar(7),GameTimestamp,126)
)
  
select d1.PlayerID, d1.GamerTag, d1.averageScore,d1.gamesPlayed, d1.averageScore -d2.averageScore as changeInScore 
from data d1 left join data d2 on d1.PlayerID = d2.PlayerID and d1.GameMonth != d2.GameMonth
where d1.GameMonth = @curMonth	
order by averageScore desc
;

select * from games g join Participation p on g.GameUUID = p.GameUUID
where p.PlayerID = '7-2-32023'
