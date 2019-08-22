import pyodbc  
import re
from SQLconnector import connectToSource
from FetchPlayerUpdatesAndNewPlayers import manualTargetSummary
from FetchPlayerAndGames import manualTargetForGames
from FetchAchievements import manualTargetAchievements
import feedbackQueue
 

def fetchIndividualWithID(id):
    
    conn = connectToSource()
    cursor = conn.cursor()
    if re.match("([0-9]+)-([0-9]+)-([0-9]+)",id):

        SQL = """select * from Players where PlayerID = ?"""
        cursor.execute(SQL,(id))
        results = cursor.fetchall()

        if len(results) >= 1:
            
            #print(results)
            feedbackQueue.q.put("Found player, updating")
            manualTargetSummary(id)
            manualTargetForGames(id)
            manualTargetAchievements(id)
            
            from BuildAchievementScoresToJSON import executeAchievementBuild
            from BuildHeadToHeadsToJSON import buildHeadToHeads
            from BuildMonthlyScoresToJSON import executeMonthlyScoresBuild
            from BuildPlayerBlob import executeBuildPlayerBlobs
            from BuildMonthlyStarQualityToJSON import executeBuildMonthlyStars
            #executeAchievementBuild()
            #executeMonthlyScoresBuild()
            #buildHeadToHeads()
            #executeBuildPlayerBlobs()
            #executeBuildMonthlyStars()
        elif len(results) == 0:
            feedbackQueue.q.put("Didn't find ID in database, performing summary search")
            manualTargetSummary(id)
    else: 
        id = "%" + id + "%"
        feedbackQueue.q.put("Didn't find player ID, searching for gamertag")
        SQL = """select PlayerID, Gamertag, Missions from Players where GamerTag like ?"""
        cursor.execute(SQL,(id))
        
        results = cursor.fetchall()
        for player in results:
            feedbackQueue.q.put ("Found player %s, gamerTag = %s, missions = %i" % (player[0], player[1], player[2]))

 
def fetchIndividual():
    ##check if it's an ID

    input() # clear the other inputs
    userInput = input('Enter a player ID or gamertag\n')
    fetchIndividualWithID(userInput)
   

