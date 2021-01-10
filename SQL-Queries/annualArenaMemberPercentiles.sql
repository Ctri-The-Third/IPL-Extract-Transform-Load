with data as (select 
percent_rank() over (order by count(distinct date_trunc('day',g.gametimestamp))) as percentile
,count(distinct date_trunc('day',g.gametimestamp)) as visits
, pl.playerID from players pl join participation p on pl.playerID = p.playerID
join games g on g.gameuuid = p.gameuuid
where g.arenaname ilike '%peter%'
and g.gametimestamp >= '2020-01-01'
and g.gametimestamp < '2021-01-01'
group by pl.playerID
),
finalresults as (
	select 0.05 as percentile, count(*) as members, min(visits)::integer as minVisits, max(visits)::integer as maxVisits from data where percentile <= 0.05
	union
	select 0.25 as percentile, count(*) as members, min(visits)::integer as minVisits, max(visits)::integer as maxVisits from data where percentile > 0.05 and percentile <= 0.25 
	union
	select 0.50 as percentile, count(*) as members, min(visits)::integer as minVisits, max(visits)::integer as maxVisits from data where percentile > 0.25 and percentile <= 0.50 
	union
	select 0.75 as percentile, count(*) as members, min(visits)::integer as minVisits, max(visits)::integer as maxVisits from data where percentile > 0.50 and percentile <= 0.75
	union
	select 0.95 as percentile, count(*) as members, min(visits)::integer as minVisits, max(visits)::integer as maxVisits from data where percentile > 0.75 and percentile <= 0.95
	union
	select 1 as percentile, count(*) as members, min(visits)::integer as minVisits, max(visits)::integer as maxVisits from data where percentile > 0.95
)
select percentile, members, minVisits, maxVisits from finalresults 
where minVisits is not null 
order by percentile


--------- games

with data as (select 
percent_rank() over (order by count(*)) as percentile
,count(*) as visits
, pl.playerID from players pl join participation p on pl.playerID = p.playerID
join games g on g.gameuuid = p.gameuuid
where g.arenaname ilike '%edin%'
and g.gametimestamp >= '2020-01-01'
and g.gametimestamp < '2021-01-01'
group by pl.playerID
),
finalresults as (
	select 0.05 as percentile, count(*) as members, min(visits)::integer as minVisits, max(visits)::integer as maxVisits from data where percentile <= 0.05
	union
	select 0.25 as percentile, count(*) as members, min(visits)::integer as minVisits, max(visits)::integer as maxVisits from data where percentile > 0.05 and percentile <= 0.25 
	union
	select 0.50 as percentile, count(*) as members, min(visits)::integer as minVisits, max(visits)::integer as maxVisits from data where percentile > 0.25 and percentile <= 0.50 
	union
	select 0.75 as percentile, count(*) as members, min(visits)::integer as minVisits, max(visits)::integer as maxVisits from data where percentile > 0.50 and percentile <= 0.75
	union
	select 0.95 as percentile, count(*) as members, min(visits)::integer as minVisits, max(visits)::integer as maxVisits from data where percentile > 0.75 and percentile <= 0.95
	union
	select 1 as percentile, count(*) as members, min(visits)::integer as minVisits, max(visits)::integer as maxVisits from data where percentile > 0.95
)
select percentile, members, minVisits, maxVisits from finalresults 
where minVisits is not null 
order by percentile


------- retention by week
with preProcess as 
(select  p.playerid
, min(g.gametimestamp) as firstSeen
, max(g.gametimestamp) as lastSeen
, floor(extract(epoch from max(g.gametimestamp) - min(g.gametimestamp))/604800)::int as weeks
from games g  join participation p on p.gameuuid = g.gameuuid
where arenaname ilike '%edin%'
and g.gametimestamp < '2021-01-01'

group by 1 
),
data as 
(
	select percent_rank() over (order by weeks) as percentile, *
	from preProcess
	where lastSeen >= '2020-01-01'
	and firstSeen < '2021-01-01'
	--where not (weeks = 0 and firstSeen < '2019-01-01')  --should scrub out players
),
finalresults as (
	select 0.05 as percentile, count(*) as members, min(weeks)::integer as minVisits, max(weeks)::integer as maxVisits from data where percentile <= 0.05
	union
	select 0.25 as percentile, count(*) as members, min(weeks)::integer as minVisits, max(weeks)::integer as maxVisits from data where percentile > 0.05 and percentile <= 0.25 
	union
	select 0.50 as percentile, count(*) as members, min(weeks)::integer as minVisits, max(weeks)::integer as maxVisits from data where percentile > 0.25 and percentile <= 0.50 
	union
	select 0.75 as percentile, count(*) as members, min(weeks)::integer as minVisits, max(weeks)::integer as maxVisits from data where percentile > 0.50 and percentile <= 0.75
	union
	select 0.95 as percentile, count(*) as members, min(weeks)::integer as minVisits, max(weeks)::integer as maxVisits from data where percentile > 0.75 and percentile <= 0.95
	union
	select 1 as percentile, count(*) as members, min(weeks)::integer as minVisits, max(weeks)::integer as maxVisits from data where percentile > 0.95
)
select percentile, members, minWeeks as minRetention, maxRetention from finalresults 
where weeks is not null 
order by percentile