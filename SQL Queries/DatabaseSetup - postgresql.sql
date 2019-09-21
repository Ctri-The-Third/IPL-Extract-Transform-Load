
/****** Object:  Table AllAchievements    Script Date: 27-Aug-19 12:19:17 ******/

CREATE TABLE AllAchievements(
    AchName varchar(50) NOT NULL,
        Description text NOT NULL,
        image varchar(64) NULL,
        ArenaName varchar(50) NOT NULL,
        AchID varchar(50) NOT NULL,
        CONSTRAINT PK_AllAchievements PRIMARY KEY  
(
    AchID
));


/****** Object:  Table Games    Script Date: 27-Aug-19 12:19:28 ******/

CREATE TABLE Games(
    GameTimestamp timestamp NOT NULL,
        GameName varchar(50) NOT NULL,
        ArenaName varchar(50) NOT NULL,
        GameUUID varchar(50) NOT NULL,
        CONSTRAINT PK_Games PRIMARY KEY 
(
    GameUUID
));
/****** Object:  Table Participation    Script Date: 27-Aug-19 12:19:38 ******/
CREATE TABLE Participation(
    PlayerID varchar(15) NOT NULL,
        GameUUID varchar(50) NOT NULL,
        Score int NOT NULL,
        insertedTimestamp timestamp NULL,
        CONSTRAINT PK_Participation PRIMARY KEY 
(
    PlayerID,GameUUID
));

/****** Object:  Table PlayerAchievement    Script Date: 27-Aug-19 12:19:45 ******/

CREATE TABLE PlayerAchievement(
    AchID varchar(50) NOT NULL,

        PlayerID varchar(50) NOT NULL,
        newAchievement int NULL,
        achievedDate date NULL,
        progressA int NULL,
        progressB int NULL,
        CONSTRAINT PK_PlayerAchievement PRIMARY KEY  
(
    AchID, PlayerID
));



/****** Object:  Table Players    Script Date: 27-Aug-19 12:19:50 ******/


CREATE TABLE Players(
    PlayerID varchar(15) NOT NULL,
        GamerTag varchar(20) NOT NULL,
        Joined date NULL,
        Missions int NULL,
        Level int NULL,
        AchievementScore int NULL,
        CONSTRAINT PK_Players PRIMARY KEY  
        (
            PlayerID
));

/****** Object:  View MostRecentGame    Script Date: 27-Aug-19 12:20:09 ******/



CREATE VIEW MostRecentGame
AS
SELECT        MAX(g.GameTimestamp) AS mostRecent, p.PlayerID
FROM            Participation AS p INNER JOIN
    Games AS g ON p.GameUUID = g.GameUUID
GROUP BY p.PlayerID;



/****** Object:  View InterestingPlayers    Script Date: 27-Aug-19 12:20:00 ******/



CREATE VIEW InterestingPlayers
AS
SELECT        Players.Missions, Players.Level, Players.PlayerID, MostRecentGame.mostRecent, 
CASE WHEN MostRecentGame.mostRecent < NOW() - INTERVAL '60 days'
    THEN 'Churned' ELSE 'Active' END AS SeenIn60Days
FROM            Players LEFT OUTER JOIN
    MostRecentGame ON Players.PlayerID = MostRecentGame.PlayerID
WHERE        (Players.Missions > 15) OR
    (Players.Level >= 4);   





