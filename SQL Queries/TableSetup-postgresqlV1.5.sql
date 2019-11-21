

/****** Object:  Table PlayerArenaSummary     ******/
CREATE TABLE PlayerArenaSummary(
    ArenaName varchar(50) NOT NULL,
	AvgStndrdScore int NOT NULL,
	missionsPlayedHere int NULL,
	levelHere int NOT NULL,
	PlayerID varchar(50) NOT NULL,
	CONSTRAINT PK_ArenaSummary PRIMARY KEY  
(
    PlayerID, ArenaName
));

