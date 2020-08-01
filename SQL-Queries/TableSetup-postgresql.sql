

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



CREATE TABLE "jobsList"
(
    "desc" text COLLATE pg_catalog."default" NOT NULL,
    id text COLLATE pg_catalog."default" NOT NULL,
    finished timestamp with time zone,
    lastHeartbeat timestamp with time zone,
    resumeIndex text COLLATE pg_catalog."default",
    started timestamp with time zone,
    Dependencies text COLLATE pg_catalog."default",
    methodName text COLLATE pg_catalog."default",
    methodParams text COLLATE pg_catalog."default",
    CONSTRAINT "jobsList_pkey" PRIMARY KEY ("id")
);
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

-- Table: public.jobslist
CREATE TABLE public.jobslist
(
    "desc" text NOT NULL,
    id text NOT NULL,
    methodname text NOT NULL,
    "started" timestamp without time zone NOT NULL,
    "finished" timestamp without time zone,
    lastHeartbeat timestamp without time zone,
    resumeindex int,
    methodparams text NOT NULL,  
    CONSTRAINT jobs_pkey PRIMARY KEY (id)
);

ALTER TABLE public.jobslist
    OWNER to "LaserScraper";


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


--1.4
-- View: public."jobsView"

ALTER TABLE jobslist
    ADD completeindex integer NULL;


CREATE OR REPLACE VIEW public."jobsView"
 AS
 WITH data AS (
         SELECT date_part('epoch'::text, now() - COALESCE(jobslist.lastheartbeat, jobslist.started)::timestamp with time zone) AS age,
            jobslist."desc",
            jobslist.id,
            jobslist.methodname,
            jobslist.started,
            jobslist.finished,
            jobslist.lastheartbeat,
            jobslist.resumeindex,
            jobslist.methodparams,
            jobslist.completeindex
           FROM jobslist
        )
 SELECT
        CASE
            WHEN data.age < 0::double precision THEN 'pending'::text
            WHEN data.age < 30::double precision THEN 'alive'::text
            WHEN data.age < 120::double precision THEN 'unhealthy'::text
            WHEN data.age > 120::double precision AND data.finished IS NULL THEN 'dead'::text
            WHEN data.age > 120::double precision AND data.finished IS NOT NULL THEN 'complete'::text
            ELSE NULL::text
        END AS healthstatus,
    data.age,
    data."desc",
    data.id,
    data.methodname,
    data.started,
    data.finished,
    data.lastheartbeat,
    data.resumeindex,
    data.methodparams,
    round((COALESCE(data.resumeindex::double precision, 0::double precision) / data.completeindex::double precision * 100::double precision)::numeric, 4) AS percenttocompletion
   FROM data
  ORDER BY data.lastheartbeat, data.started;

ALTER TABLE public."jobsView"
    OWNER TO "LaserScraper";

