declare @startDate as date
set @startDate = '2019-08-01'

select  * from InterestingPlayers
where mostRecent < DATEADD(day, -61, @startDate)
order by Level desc, Missions desc, SeenIn60Days Asc