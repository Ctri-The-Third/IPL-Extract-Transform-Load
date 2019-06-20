import pyodbc
import uuid


from SQLconnector import connectToSource

def addPlayer(playerID,GamerTag,Joined,missions,level):

    conn = connectToSource()
    cursor = conn.cursor()

    query = """select * from LaserScraper.dbo.Players 
    where playerID = '{0}' """.format(playerID)
    cursor.execute (query)
    print("Query = {0}".format(query))
    result = cursor.fetchone()
    print("Result = {0}".format(result))

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

