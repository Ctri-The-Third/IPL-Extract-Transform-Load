

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

ALTER TABLE AllAchievements ALTER COLUMN AchName TYPE varchar(100);


-- View: public."participationWithStars"

CREATE OR REPLACE VIEW public."participationWithStars" AS 
 WITH data AS (
         SELECT pl.playerid,
            pl.gamertag,
            g.gamename,
            g.gametimestamp,
            g.arenaname,
            p.score,
            row_number() OVER (PARTITION BY g.gametimestamp, g.arenaname ORDER BY g.gametimestamp DESC, p.score DESC) AS rank,
            count(p.playerid) OVER (PARTITION BY g.gametimestamp, g.arenaname ORDER BY g.gametimestamp DESC) AS playercount,
            to_char(g.gametimestamp, 'YYYY-MM'::text) AS gamemonth
           FROM participation p
             JOIN games g ON p.gameuuid::text = g.gameuuid::text
             JOIN players pl ON p.playerid::text = pl.playerid::text
        ), datawithstars AS (
         SELECT data.playerid,
            data.gamertag,
            data.gamename,
            data.gametimestamp,
            data.arenaname,
            data.score,
            data.rank,
            data.playercount,
            data.gamemonth,
            data.playercount * data.playercount / data.rank AS starsforgame
           FROM data
        )
 SELECT datawithstars.playerid,
    datawithstars.gamertag,
    datawithstars.gamename,
    datawithstars.gametimestamp,
    datawithstars.arenaname,
    datawithstars.score,
    datawithstars.rank,
    datawithstars.playercount,
    datawithstars.gamemonth,
    datawithstars.starsforgame
   FROM datawithstars;

ALTER TABLE public."participationWithStars"
  OWNER TO "LaserScraper";
