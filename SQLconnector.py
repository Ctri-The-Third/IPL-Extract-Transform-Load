import pyodbc



def connectToSource():

    conn = pyodbc.connect('Driver={SQL Server}; Server=CTRI-DESKTOP\SQLEXPRESS; Database=LaserScraper; Trusted_Connection=yes;')
    return conn

def addPlayer(playerID,GamerTag,Joined,missions):

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
        (PlayerID,GamerTag,Joined,Missions)
        VALUES
        (?,?,?,?);""" 
        cursor.execute(query,[playerID,GamerTag,Joined,missions])
        print("Added player {0}!".format(playerID))
    else:
        query = """update LaserScraper.dbo.Players
        SET Missions = ?
        WHERE PlayerID = ?"""
        response = cursor.execute(query,[missions,playerID])
        print("Updated player {0}, {1}!".format(playerID,response))

    conn.commit()
    conn.close()

def addGame(timestamp, arena, gametype):
    # returns UUID of existing game if already exists, otherwise creates
    return ''

def addParticipation(gameUUID, playerID, score):
    # doesn't return anything
    return ''

