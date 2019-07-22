with IPs as (

select playerID from InterestingPlayers

) 
update players set Missions = Missions - 1 
where Players.PlayerID in (IPs.playerID)