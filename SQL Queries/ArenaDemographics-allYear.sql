with playerMetrics as (
    select gamertag,arenaname,min(gametimestamp) as firstGame ,max(gametimestamp) as lastGame , count(*) 
    from participation p 
    join players pl on p.playerID = pl.playerID
    join games g on p.gameuuid = g.gameuuid
    group by 1,2


),
playerMissions as (
    select playerID, count(*) from participation p  
)
select 
--     count (*)
--   , count (case when firstGame > '2019-01-01' then 1 else null end) as newPlayers
--   , count (case when (firstGame < '2019-08-01' and lastGame < '2019-09-01' and lastgame > '2019-01-01') then 1 else null end ) as churnedPlayers
* 
from playerMetrics
where firstgame < '2019-08-01'
and lastGame < '2019-09-01'
and lastGame > '2019-01-01'

--firstPlayed
--lastPlayed
--playerID

