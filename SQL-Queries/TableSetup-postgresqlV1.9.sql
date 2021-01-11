
CREATE OR REPLACE VIEW public.interestingplayers AS
 WITH maxlevels AS (
         SELECT playerarenasummary.playerid,
            max(playerarenasummary.locallevel) AS level
           FROM playerarenasummary
          GROUP BY playerarenasummary.playerid
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
     LEFT JOIN maxlevels pas ON players.playerid::text = pas.playerid::text
  WHERE players.missions > 15 OR pas.level >= 4;

ALTER TABLE public.interestingplayers
    OWNER TO "LaserScraper";



