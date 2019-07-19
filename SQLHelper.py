import pyodbc
import uuid
import csv 

from SQLconnector import connectToSource



def getInterestingPlayersRoster(includeChurned,startDate,period):

    conn = connectToSource()
    cursor = conn.cursor()
    if includeChurned == True:
        query = """
        select  * from InterestingPlayers
        order by Level desc, Missions desc, SeenIn60Days Asc
        """
        cursor.execute(query)
    else:
        query = """
    declare @startDate as date
    declare @period as int
    set @startDate = ?
    set @period = ?

    select  * from InterestingPlayers
    where mostRecent > DATEADD(day, -@period, @startDate)
    order by Level desc, Missions desc, SeenIn60Days Asc
        """

        cursor.execute(query,(startDate,period))
    results = cursor.fetchall()
    playerList = []
    for result in results:
        #print (result[0])
        playerList.append(result[2])

    conn.commit()
    conn.close()
    return playerList
    

def addPlayer(playerID,GamerTag,Joined,missions,level):

    conn = connectToSource()
    cursor = conn.cursor()

    query = """select * from LaserScraper.dbo.Players 
    where playerID = '{0}' """.format(playerID)
    cursor.execute (query)
    
    result = cursor.fetchone()
    
    
    if result == None:
        query =  """insert into LaserScraper.dbo.Players 
        (PlayerID,GamerTag,Joined,Missions,Level)
        VALUES
        (?,?,?,?,?);""" 
        cursor.execute(query,[playerID,GamerTag,Joined,missions,level])
        
        print("  DBG: SQLHelper.AddPlayer - Added new player %s" % playerID)
        conn.commit()
        conn.close()
        return 1 
    elif  result[3] != missions:
        query = """update LaserScraper.dbo.Players
        SET Missions = ?,
        Level = ?
        WHERE PlayerID = ?"""
        cursor.execute(query,[missions,level,playerID])
        
        print("  DBG: SQLHelper.AddPlayer - Updated player's missions [%s] to [%s]" % (result[3],missions))
        conn.commit()
        conn.close()
        return 2
    else: 
        
        #print("  DBG: SQLHelper.AddPlayer - No change to missions, no change.")
        conn.commit()
        conn.close()
        return 0
        


def addGame(timestamp, arena, gametype):
    # returns UUID of existing game if already exists, otherwise creates
    # games are never updated.
    
    conn = connectToSource()
    cursor = conn.cursor()
    query = """select GameTimestamp, GameUUID from LaserScraper.dbo.Games 
    where GameTimestamp = convert(datetime,?,20) AND 
    GameName = ? AND
    ArenaName = ?"""
    cursor.execute(query,(timestamp,gametype,arena))
    result = cursor.fetchone()

    if result == None :
        query = """INSERT INTO LaserScraper.dbo.Games
        (GameTimestamp, ArenaName, GameName, GameUUID) 
        VALUES
        (CONVERT(datetime,?,20),?,?,?)
        """
        gameUUID = str(uuid.uuid4())
        cursor.execute(query,(timestamp,arena,gametype,gameUUID))
        #print ("SQLconnector.insertGame: Insert game check added a game! : %s" % result)
        conn.commit()
        conn.close()
    else: 
         #print ("SQLconnector: Insert game check found an exiting game! : %s" % result)
         return result.GameUUID

    return ''

def addParticipation(gameUUID, playerID, score):
    conn = connectToSource()
    cursor = conn.cursor()
    query = """select count (*) from LaserScraper.dbo.Participation
    where GameUUID = ? AND 
    PlayerID = ?"""
    cursor.execute(query,(gameUUID,playerID))
    result = cursor.fetchone()

    if result[0] == 0 :
        query = """INSERT INTO LaserScraper.dbo.Participation
        (GameUUID, PlayerID, Score) 
        VALUES
        (?,?,?)
        """
        result = cursor.execute(query,(gameUUID,playerID,score))
        #print ("SQLconnector.addParticipation: Added player to game! : %s" % gameUUID)
        conn.commit()
    #else: 
        #print ("SQLconnector.addParticipation: We already know this player played this game! : %s" % gameUUID)

    
    conn.close()
    return ''

def addAchievement(achName, Description, image):
    #do something
    conn =  connectToSource()
    cursor = conn.cursor()
    query = """
    SELECT *
    FROM AllAchievements
    where image = ? 
    and achName = ?
    """
    results = cursor.execute(query,(image,achName))
    result = results.fetchone()

    if result == None:
        #print("SQLHelper.addAchievement: Didn't find [{0}], adding it".format(achName))
        query = """
        INSERT into AllAchievements
         (AchName, image, Description)
        VALUES (?,?,?)
        
        """
        cursor.execute(query,(achName,image,Description))
        #print ("SQLHelper.addAchievement: Added it!")
        conn.commit()
        conn.close()

    #else:
        #print ("SQLHelper.addAchievement: found [{0}], no changes to it".format(achName))

    #print(result)

def addPlayerAchievement(image,playerID,newAchievement,achievedDate,progressA,progressB):
#do something
    conn =  connectToSource()
    cursor = conn.cursor()
    query = """
    SELECT *
    FROM PlayerAchievement
    where image = ? 
    and playerID = ?
    """
    results = cursor.execute(query,(image,playerID))
    result = results.fetchone()
    if achievedDate == "0000-00-00" :
        achievedDate = None
    if result == None:
        #print("SQLHelper.addPlayerAchievement: Player has just discvered this, adding it")
        
        query = """
        insert into PlayerAchievement
        (Image,PlayerID,newAchievement,achievedDate,progressA,progressB)
        VALUES ( ?, ?, ?, ?, ?, ?)
        

        """
        results = cursor.execute(query,(image,playerID,newAchievement,achievedDate,progressA,progressB))
    else:
        
        #print("SQLHelper.addPlayerAchievement: found achievement progress, updating it")
        query = """
        UPDATE PlayerAchievement
        SET newAchievement = ?, 
        achievedDate = ?,
        progressA = ?,
        progressB = ?

        WHERE Image = ? 
        AND PlayerID = ?

        """
        results = cursor.execute(query,(newAchievement,achievedDate,progressA,progressB,image,playerID))
        #print(image)
    conn.commit()
    conn.close()

def addPlayerAchievementScore (playerID, score):
    conn = connectToSource()
    cursor = conn.cursor()
    query = "select playerID from players where playerID = ? "
    cursor.execute(query,(playerID))

    if cursor.fetchone() == None:
        print("[Warning] SQLHelper.addPlayerAchievementScore didn't find the player, could not update score")
    else:
        #print ("SQLHelper.addPlayerAchievementScore found the player, updating their achievement score")
        query = "update players set AchievementScore = ? where playerID = ?"
        cursor.execute(query,(score,playerID))

    conn.commit()
    conn.close()

def getTop5PlayersRoster(startDate,endDate):
    conn = connectToSource()
    cursor = conn.cursor()
    query = """DECLARE @startDate as date
DECLARE @endDate as date;
SET @startDate = ?;
SET @endDate = ?;

with PlayersInGame as (
	SELECT 
	Count (Players.GamerTag) as playersInGame, 
	Games.GameUUID as gameID
	FROM [LaserScraper].[dbo].[Games] as Games
	join Participation on participation.GameUUID = Games.GameUUID
	join Players on Participation.PlayerID = Players.PlayerID
	where GameTimestamp >= @startDate
	and GameTimeStamp < @endDate
	group by Games.GameUUID ),
averageOpponents as 
(
	select avg(cast(playersInGame as float)) as AverageOpponents,  players.PlayerID from Participation 
	join PlayersInGame on Participation.GameUUID = PlayersInGame.gameID
	join Games on Games.GameUUID = PlayersInGame.gameID
	join Players on Participation.PlayerID = players.PlayerID
	group by  players.PlayerID
		
),
totalGamesPlayed as 
(
	select count(*) as gamesPlayed,  Participation.PlayerID
	from Participation 
	join Games on Games.GameUUID = Participation.GameUUID
	where GameTimestamp >= @startDate
	and GameTimeStamp < @endDate
	group by Participation.PlayerID
),
Ranks as 
(
	select GameTimestamp, GameName, Players.PlayerID, GamerTag, Score, 
		ROW_NUMBER() over (partition by GameTimestamp order by score desc) as gamePosition
	from Games 

	join Participation on Games.GameUUID = Participation.GameUUID
	join Players on Participation.PlayerID = Players.PlayerID
	where GameTimestamp >= @startDate
	and GameTimeStamp < @endDate
),
AverageRanks as 
( select PlayerID, AVG(CONVERT(float,gamePosition)) as AverageRank from Ranks
	group by PlayerID), 
AverageScores as (
	SELECT 
	Players.PlayerID, 	
	avg(Score) as averageScore
	
	FROM Participation
	inner join Players on Participation.PlayerID = Players.PlayerID
	inner join Games on Participation.GameUUID = Games.GameUUID
	join totalGamesPlayed on totalGamesPlayed.PlayerID = Players.PlayerID
	join averageOpponents on averageOpponents.PlayerID = Players.PlayerID
	join AverageRanks on AverageRanks.PlayerID = Players.PlayerID
	where Games.GameTimestamp >= @startDate
	AND Games.GameTimestamp < @endDate
	and Games.GameName in ('Team','3 Teams','4 Teams', 'Colour Ranked','Individual')
	group by Players.PlayerID
 ),
StarQuality as
(
	SELECT  Players.PlayerID, GamerTag, round(AverageOpponents,2) as AverageOpponents, gamesPlayed, round(AverageRank,2) as AverageRank, 
	round((AverageOpponents *  1/(AverageRank/AverageOpponents)),2) as AvgQualityPerGame,
	round((AverageOpponents * gamesPlayed * 1/(AverageRank/AverageOpponents)),2) as TotalQualityScore, averageScore, AchievementScore
	from Players
	join totalGamesPlayed on totalGamesPlayed.PlayerID = Players.PlayerID
	join averageOpponents on averageOpponents.PlayerID = Players.PlayerID
	join AverageRanks on AverageRanks.PlayerID = Players.PlayerID
	left join AverageScores on AverageScores.PlayerID = Players.PlayerID
	

),
GoldenTop3 as 
(
	select top (3) PlayerID, ROW_NUMBER() over (order by avgQualityPerGame desc) as playerRank from StarQuality
	order by AvgQualityPerGame desc
),
BestScorer as (
	SELECT top (1) PlayerID --, GamerTag, round(AverageOpponents,2) as AverageOpponents, gamesPlayed, round(AverageRank,2) as AverageRank, 
	--round((AverageOpponents *  1/(AverageRank/AverageOpponents)),2) as AvgQualityPerGame,
	--round((AverageOpponents * gamesPlayed * 1/(AverageRank/AverageOpponents)),2) as TotalQualityScore, averageScore, AchievementScore
	
	from AverageScores 
	where PlayerID not in (select PlayerID from GoldenTop3) 
	order by averageScore desc
),
BestAchiever as(
	SELECT top(1) Players.PlayerID
	--GamerTag, round(AverageOpponents,2) as AverageOpponents, gamesPlayed, round(AverageRank,2) as AverageRank, 
	--round((AverageOpponents *  1/(AverageRank/AverageOpponents)),2) as AvgQualityPerGame,
	--round((AverageOpponents * gamesPlayed * 1/(AverageRank/AverageOpponents)),2) as TotalQualityScore, averageScore, AchievementScore
	
	from Players
	join totalGamesPlayed on totalGamesPlayed.PlayerID = Players.PlayerID
	
	where players.PlayerID not in (select PlayerID from GoldenTop3) and Players.PlayerID not in (select PlayerID from BestScorer)
	order by Players.AchievementScore desc
)

select p.PlayerID , GamerTag, playerRank, 'Top3' as source from GoldenTop3 p
join Players pl on pl.PlayerID = p.PlayerID
union 
select  p.PlayerID , GamerTag, 4 as playerRank, 'BestScorer' as source from BestScorer p
join Players pl on pl.PlayerID = p.PlayerID
union 
select  p.PlayerID , GamerTag, 5 as playerRank, 'BestAchiever' as source from BestAchiever p
join Players pl on pl.PlayerID = p.PlayerID
order by playerRank asc

"""
    cursor.execute(query,(startDate,endDate))
    rows = cursor.fetchall()
    if rows == None:
        print("[Warning] SQLHelper.getTop5Players didn't find any players. Is there data in all tables?/")
    else:
        print ("SQLHelper.getTop5Players found all 5 players")

    conn.commit()
    conn.close()
    return rows

def dumpParticipantsAndGamesToCSV():
    conn = connectToSource()
    cursor = conn.cursor()
    query = """select * From Participation"""
    cursor.execute(query)
    count = 0 
    file = open("CSV dump - participation","w+")
    for row in cursor.fetchall():
        count = count + 1
        file.write("%s,%s,%i\n" % (row[0],row[1],row[2]))
    file.close()
    
    print("Dumped %i rows to CSV dump - participation.csv" % (count))
    query = """select * From Games"""
    cursor.execute(query)
    count = 0 
    file = open("CSV dump - Games","w+")
    for row in cursor.fetchall():
        count = count + 1
        file.write("%s,%s,%s\n" % (row[0],row[1],row[2]))
    file.close()
    conn.close()
    print("Dumped %i rows to CSV dump - Games.csv" % (count))



def impParticipantsAndGamesToCSV():
    print("Not implemented yet")

    conn = connectToSource()
    cursor = conn.cursor()
    Query = """BULK INSERT """

