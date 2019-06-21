    select playerID, Gamertag, players.Level, Missions 
    from players
    where (Level = 6) 
    or (Level = 5) 
    or players.Missions >= 15
    order by Level desc, Missions desc