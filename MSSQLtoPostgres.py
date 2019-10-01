#DataShunter
import psycopg2
import pyodbc

PGconn = psycopg2.connect(host='localhost',port=5432 ,user='LaserScraper', password='LaserScraper', database = 'laserscraper')
MSconn = pyodbc.connect('Driver={SQL Server}; Server=CTRI-DESKTOP\SQLEXPRESS; Database=LaserScraper; Trusted_Connection=yes;')

PGCursor = PGconn.cursor()
MSCursor = MSconn.cursor()

def Players():
    MSQuery = "Select * from Players"
    MSResults = MSCursor.execute(MSQuery)
    for row in MSResults.fetchall():
        print(row)
        PGQuery = """INSERT into Players (playerid,gamertag,joined,missions,level,achievementscore) 
        VALUES (%s,%s,%s,%s,%s,%s);"""
        try:
            PGCursor.execute(PGQuery,(row[0],row[1],row[2],row[3],row[4],row[5]))
            print("Added %s to DB" % (row[0])) 
        except psycopg2.Error as e:
            print ("Bounced %s from DB: %s"% (row[0],e.pgerror))
            PGconn.rollback()

def Games():
    MSQuery = "Select * from Games"
    MSResults = MSCursor.execute(MSQuery)
    for row in MSResults.fetchall():
        print(row)
        PGQuery = """INSERT into Games (gametimestamp,gamename,arenaname,gameuuid) 
        VALUES (%s,%s,%s,%s);"""
        try:
            PGCursor.execute(PGQuery,(row[0],row[1],row[2],row[3]))
            print("Added %s to DB" % (row[3])) 
        except psycopg2.Error as e:
            print ("Bounced %s from DB: %s"% (row[3],e.pgerror))
            PGconn.rollback()

def Participation():
    MSQuery = "Select * from Participation"
    MSResults = MSCursor.execute(MSQuery)
    for row in MSResults.fetchall():
        print(row)
        PGQuery = """INSERT into Participation (playerid,gameuuid,score,insertedtimestamp) 
        VALUES (%s,%s,%s,%s);"""
        try:
            PGCursor.execute(PGQuery,(row[0],row[1],row[2],row[3]))
            print("Added %s|%s to DB" % (row[0],row[1])) 
        except psycopg2.Error as e:
            print ("Bounced %s|%s from DB: %s"% (row[0],row[1],e.pgerror))
            PGconn.rollback()

def Participation():
    MSQuery = "Select * from Participation"
    MSResults = MSCursor.execute(MSQuery)
    for row in MSResults.fetchall():
        print(row)
        PGQuery = """INSERT into Participation (playerid,gameuuid,score,insertedtimestamp) 
        VALUES (%s,%s,%s,%s);"""
        try:
            PGCursor.execute(PGQuery,(row[0],row[1],row[2],row[3]))
            print("Added %s|%s to DB" % (row[0],row[1])) 
        except psycopg2.Error as e:
            print ("Bounced %s|%s from DB: %s"% (row[0],row[1],e.pgerror))
            PGconn.rollback()

def AllAchievements():
    MSQuery = "Select * from AllAchievements"
    MSResults = MSCursor.execute(MSQuery)
    for row in MSResults.fetchall():
        print(row)
        PGQuery = """INSERT into AllAchievements (achname,description,image,arenaname,achid) 
        VALUES (%s,%s,%s,%s,%s);"""
        try:
            PGCursor.execute(PGQuery,(row[0],row[1],row[2],row[3],row[4]))
            print("Added %s|%s to DB" % (row[0],row[3])) 
        except psycopg2.Error as e:
            print ("Bounced %s|%s from DB: %s"% (row[0],row[3],e.pgerror))
            PGconn.rollback()


def PlayerAchievement():
    MSQuery = "Select * from PlayerAchievement"
    MSResults = MSCursor.execute(MSQuery)
    for row in MSResults.fetchall():
        print(row)
        PGQuery = """INSERT into PlayerAchievement (achid,playerid,achieveddate) 
        VALUES (%s,%s,%s);"""
        try:
            PGCursor.execute(PGQuery,(row[0],row[1],row[3]))
            print("Added %s|%s to DB" % (row[0],row[1])) 
        except psycopg2.Error as e:
            print ("Bounced %s|%s from DB: %s"% (row[0],row[1],e.pgerror))
            PGconn.rollback()
Players()
Games()
Participation()
AllAchievements()
PlayerAchievement()




