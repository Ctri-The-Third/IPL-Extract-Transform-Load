--4 placeholders. See comments.
with data as  ( 
  SELECT
	p.PlayerID, 
	GamerTag, 
	avg(Score) as averageScore,
	count(GamerTag) as gamesPlayed,
	to_char(GameTimestamp,'YYYY-MM') as GameMonth
	
  FROM Participation p
  inner join Players pl on p.PlayerID = pl.PlayerID
  inner join Games g on p.GameUUID = g.GameUUID
  where to_char(GameTimestamp,'YYYY-MM') in  ('2019-09','2019-10') --This month, and Last month

  and (
	g.GameName in ('Team','3 Teams','4 Teams', 'Colour Ranked','Individual')
    or g.GameName in ('Standard - Solo', 'Standard - Team','Standard [3 Team] (10)','Standard [3 Team] (15)','Standard 2 Team',
    'Standard 3 Team','Standard 4 Team','Standard Individual','Standard Multi team','- Standard [2 Team] (15))')
	)
  and g.ArenaName = 'Funstation Ltd, Edinburgh, Scotland' --target arena
  GROUP BY p.PlayerID, pl.GamerTag, to_char(GameTimestamp,'YYYY-MM') 
)


select d1.PlayerID, d1.GamerTag, cast(d1.averageScore as int),d1.gamesPlayed, round(cast(d1.averageScore -d2.averageScore as numeric),2) as changeInScore 
from data d1 left join data d2 on d1.PlayerID = d2.PlayerID and d1.GameMonth != d2.GameMonth
where d1.GameMonth = '2019-10'  --this month
order by averageScore desc;
