

/****** Object:  Table PlayerArenaSummary     ******/
CREATE TABLE PlayerArenaSummary(
    ArenaName varchar(50) NOT NULL,
	PlayerID varchar(50) NOT NULL,
	localAvgStdScore int NOT NULL,
	localMissions int NULL,
	localLevel int NOT NULL,
	CONSTRAINT PK_PlayerArenaSummary PRIMARY KEY  
(
    PlayerID, ArenaName
));

CREATE TABLE ArenaRanksLookup (
	ArenaName varchar(50) not null,
	rankNumber int not null
	rankName varchar(50) not null
	CONSTRAINT PK_ArenaRanksLookup PRIMARY KEY
	(
		ArenaName, rankNumber
	)
);

CREATE OR REPLACE VIEW public."playerHomes"
  AS
  
  with data as (
    select 
    to_char(gametimestamp, 'IYYY-MM') as month
    , count(*) as gameCount
    , p.playerID
    , arenaName
    from players pl
    join participation p on pl.playerID = p.playerID
    join games g on p.gameuuid = g.gameuuid
    group by 1,3,4
    order by 1 desc,3,2 desc )
  select row_number() over (partition by month, playerID order by gameCount desc) as arenaRow, * from data
  order by month desc, playerID desc, gameCount desc"""
