select pl1.GamerTag as Player, pl2.GamerTag as oppopnent, count(*) as timesPlayedTogether 
from Participation pa1 
join Players pl1 on pa1.PlayerID = pl1.PlayerID
join Participation pa2 on pa2.GameUUID = pa1.GameUUID 
	and pa1.PlayerID != pa2.PlayerID
join Players pl2 on pa2.PlayerID = pl2.PlayerID
join InterestingPlayers ip on pa1.PlayerID = ip.playerID
where  SeenIn60Days = 'Active'
group by pl1.PlayerID, pl1.GamerTag, pa2.playerID, pl2.GamerTag 
order by timesPlayedTogether desc