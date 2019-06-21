import pyodbc
import uuid


from SQLconnector import connectToSource

def getInterestingPlayersRoster():

    conn = connectToSource()
    cursor = conn.cursor()

    query = """
    select playerID, Gamertag, players.Level, Missions 
    from players
    where (Level = 6) 
    or (Level = 5) 
    or players.Missions > 15
    order by Level desc, Missions desc
    """

    results = cursor.execute(query)
    playerList = []
    for result in results:
        #print (result[0])
        playerList.append(result[0])
    return playerList



def addPlayer(playerID,GamerTag,Joined,missions,level):

    conn = connectToSource()
    cursor = conn.cursor()

    query = """select * from LaserScraper.dbo.Players 
    where playerID = '{0}' """.format(playerID)
    cursor.execute (query)
    #print("Query = {0}".format(query))
    result = cursor.fetchone()
    #print("Result = {0}".format(result))

    if result == None:
        query =  """insert into LaserScraper.dbo.Players 
        (PlayerID,GamerTag,Joined,Missions,Level)
        VALUES
        (?,?,?,?,?);""" 
        cursor.execute(query,[playerID,GamerTag,Joined,missions,level])
        print("Added player {0}!".format(playerID))
    else:
        query = """update LaserScraper.dbo.Players
        SET Missions = ?,
        Level = ?
        WHERE PlayerID = ?"""
        response = cursor.execute(query,[missions,level,playerID])
        print("Updated player {0}, {1}!".format(playerID,response))

    conn.commit()
    conn.close()

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
        print("SQLHelper.addAchievement: Didn't find [{0}], adding it".format(achName))
        query = """
        INSERT into AllAchievements
         (AchName, image, Description)
        VALUES (?,?,?)
        
        """
        cursor.execute(query,(achName,image,Description))
        print ("SQLHelper.addAchievement: Added it!")
        conn.commit()
        conn.close()

    else:
        print ("SQLHelper.addAchievement: found [{0}], no changes to it".format(achName))

    print(result)

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
        print("SQLHelper.addPlayerAchievement: Player has just discvered this, adding it")
        
        query = """
        insert into PlayerAchievement
        (Image,PlayerID,newAchievement,achievedDate,progressA,progressB)
        VALUES ( ?, ?, ?, ?, ?, ?)
        

        """
        results = cursor.execute(query,(image,playerID,newAchievement,achievedDate,progressA,progressB))
    else:
        
        print("SQLHelper.addPlayerAchievement: found achievement progress, updating it")
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
        print(image)
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
        print ("SQLHelper.addPlayerAchievementScore found the player, updating their achievement score")
        query = "update players set AchievementScore = ? where playerID = ?"
        cursor.execute(query,(score,playerID))

    conn.commit()
    conn.close()