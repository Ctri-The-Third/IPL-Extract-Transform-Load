

/****** Object:  Table PlayerArenaSummary     ******/
CREATE TABLE PlayerArenaSummary(
    ArenaName varchar(50) NOT NULL,
	PlayerID varchar(50) NOT NULL,
	localAvgStdScore int NOT NULL,
	localMissions int NULL,
	localLevel int NOT NULL,
	CONSTRAINT PK_ArenaSummary PRIMARY KEY  
(
    PlayerID, ArenaName
));

