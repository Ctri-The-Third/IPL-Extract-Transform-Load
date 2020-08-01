--4 placeholders. See comments.
with data as  ( 
  SELECT
	p.PlayerID, 
	GamerTag, 
	Score,
	g.gamename ,
	to_char(GameTimestamp,'YYYY-MM') as GameMonth,
	gametimestamp
	
  FROM Participation p
  inner join Players pl on p.PlayerID = pl.PlayerID
  inner join Games g on p.GameUUID = g.GameUUID
  where to_char(GameTimestamp,'YYYY-MM') in  ('2019-10') --This month

  and (
	g.GameName in ('Team','3 Teams','4 Teams', 'Colour Ranked','Individual')
    or g.GameName in ('Standard - Solo', 'Standard - Team','Standard [3 Team] (10)','Standard [3 Team] (15)','Standard 2 Team',
    'Standard 3 Team','Standard 4 Team','Standard Individual','Standard Multi team','- Standard [2 Team] (15))')
	)
  and g.ArenaName = 'Funstation Ltd, Edinburgh, Scotland' --target arena
	and p.playerID = '9-6-106' --target player
)
select * from data order by gametimestamp desc 
