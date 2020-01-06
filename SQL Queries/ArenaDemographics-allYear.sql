with playerMetrics as (
    select gamertag
    , pl.playerID
    , arenaname
    , min(gametimestamp) as firstGame 
    , max(gametimestamp) as lastGame 
    from participation p 
    join players pl on p.playerID = pl.playerID
    join games g on p.gameuuid = g.gameuuid
    where arenaName ilike '%edinburgh%'
    group by gamerTag, pl.playerID, arenaName
),
playerMissions as (
    select playerID, count(*) as gamesPlayedInPeriod from participation p  join games g on p.gameuuid = g.gameuuid
    where gametimestamp >= '2019-06-01'
    and gametimestamp < '2020-01-01'
    group by 1
)
select 
     count (case when gamesPlayedInPeriod > 0 then 1 else null end) as totalPlayingPlayers
   , count (case when firstGame >= '2019-06-01' then 1 else null end) as newPlayers
   , count (case when ((lastGame < to_date('2020-01-01','YYYY-MM-DD') - INTERVAL '60 days' ) and lastGame >= '2019-06-01' ) then 1 else null end ) as churnedPlayers 
from playerMetrics pm1 join playerMissions pm2 on pm1.playerID = pm2.playerID


--firstPlayed
--lastPlayed
--playerID
