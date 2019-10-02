/* 

--- DO NOT UPLOAD TO SOURCE CONTROL ---
By request of Darklight Ltd, they have kindly asked us not to share the handicap calculations.

*/

declare @handicapConstant as float
declare @lag as float
declare @old as float
declare @startDate as date
declare @arenaName as varchar(255)
set @handicapConstant = 30
set @lag = 5;
set @old = 1
set @startDate = '2019-05-23';
set @arenaName = 'Funstation Ltd, Edinburgh, Scotland'

with data as ( 
	select  pl.PlayerID
	, g.GameUUID
	, GameTimestamp
	, lead(g.GameUUID) over (partition by pl.PlayerID order by GameTimestamp asc) as nextGameuuid  --the player's next game.
	, lead(GameTimestamp) over (partition by pl.PlayerID order by GameTimestamp asc) as nextGametimestamp  --timestamp of the player's next game
	, ROW_NUMBER() over (partition by GameTimestamp order by GameTimestamp desc, score desc)  as rank,  
	count(p.PlayerID) over (partition by GameTimestamp order by GameTimestamp desc) as playerCount
	from Participation p join Games g on p.GameUUID = g.GameUUID 
	join Players pl on p.PlayerID = pl.PlayerID
	
	where GameTimestamp > @startDate and
	g.ArenaName = @arenaName
	
),
firstGames as  --for anchoring the recursion
( 
	select PlayerID, min(GameTimestamp) as firstGameTimestamp
	from data
	group by PlayerID
)
,handicap as ( 
	select  --the anchor games (first games played, handicap = 1)
		d.PlayerID
		, GameUUID
		, nextGameuuid
		, GameTimestamp
		, rank
		, playerCount
		, (((1 * (@lag - 1)) + (1 + ((((@handicapConstant/playerCount) * rank) - (0.2 * (@handicapConstant/playerCount))) - 0.5 * @handicapConstant) / @handicapConstant) * 1) / @lag) as newH
	from data d inner join firstGames fg on d.GameTimestamp = fg.firstGameTimestamp and d.PlayerID = fg.PlayerID

union all

	select -- the recursive select
		d.PlayerID
		, d.GameUUID
		, d.nextGameuuid
		, d.GameTimestamp
		, d.rank
		, d.playerCount
		, (((h.newH * (@lag - 1)) + (1 + ((((@handicapConstant/h.playerCount) * h.rank) - (0.2 * (@handicapConstant/h.playerCount))) - 0.5 * @handicapConstant) / @handicapConstant) * h.newH) / @lag) as newH

	from handicap h inner join data d on h.nextGameuuid = d.GameUUID and h.PlayerID = d.PlayerID
	--select from itself, using the "next" values to link with a record in the data view, then bringing that data (D) info into the handicap (H) expression.
)

--now output the info.
select pl.PlayerID, GamerTag, newH as DarkLightHandicap from handicap h join players pl on h.PlayerID = pl.PlayerID
where nextGameuuid is null
order by newH asc
OPTION (MAXRECURSION 300) --there will need to be one recurrsion for game a player plays.


