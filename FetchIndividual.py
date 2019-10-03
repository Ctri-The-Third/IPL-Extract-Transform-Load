
import re
from SQLconnector import connectToSource
from FetchPlayerUpdatesAndNewPlayers import manualTargetSummary
from FetchPlayerAndGames import manualTargetForGames
from FetchAchievements import manualTargetAchievements
import feedbackQueue
import ConfigHelper as cfg
 

def fetchIndividualWithID(id):
    prefix = cfg.getConfigString("ID Prefix")
    conn = connectToSource()
    cursor = conn.cursor()

    SQL = """select PlayerID from Players where PlayerID = %s or PlayerID =%s%s or GamerTag like %s order by missions desc limit 1"""
    
    data = (id,prefix,id,'%%%s%%' % (id))
    print (SQL % data)
    cursor.execute(SQL,data)
    results = cursor.fetchone()

    if len(results) == 1:
        
        #print(results)
        feedbackQueue.q.put("Found player, updating")
        id = results[0]
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

 
def fetchIndividual():
    ##check if it's an ID

    input() # clear the other inputs
    userInput = input('Enter a player ID or gamertag\n')
    fetchIndividualWithID(userInput)
   

