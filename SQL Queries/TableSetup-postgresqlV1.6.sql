

CREATE OR REPLACE VIEW public."interestingplayers"
  AS
  
  with maxLevels as 
  ( select playerID, max (localLevel) as level 
  from playerarenasummary
  group by 1
  )
  SELECT players.missions,
      pas.level,
      players.playerid,
      mostrecentgame.mostrecent,
          CASE
              WHEN mostrecentgame.mostrecent < (now() - '60 days'::interval) THEN 'Churned'::text
              ELSE 'Active'::text
          END AS seenin60days
    FROM players
      LEFT JOIN mostrecentgame ON players.playerid::text = mostrecentgame.playerid::text
    Left Join maxLevels pas ON players.playerid::text = pas.playerid::text
    WHERE players.missions > 15 OR pas.level >= 4;