
import re
from SQLconnector import connectToSource
from FetchPlayerUpdatesAndNewPlayers import manualTargetSummary, manualTargetSummaryAndIncludeRank
from FetchPlayerAndGames import manualTargetForGames
from FetchAchievements import manualTargetAchievements
import feedbackQueue
import ConfigHelper as cfg
 

def fetchIndividualWithID(id):
    
    conn = connectToSource()
    cursor = conn.cursor()

    SQL = """select PlayerID from Players where PlayerID = %s or PlayerID =%s%s or GamerTag ilike %s order by missions desc limit 1"""
    prefix = cfg.getConfigString("ID Prefix")
    data = (id,prefix,id,'%%%s%%' % (id))
    #print (SQL % data)
    cursor.execute(SQL,data)
    results = cursor.fetchone()

    if results is not None and len(results) == 1:
        
        #print(results)
        feedbackQueue.q.put("Found player, updating")
        id = results[0]
        manualTargetSummaryAndIncludeRank(id)
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
    elif results is None:
        feedbackQueue.q.put("Didn't find ID in database, performing summary search")
        manualTargetSummary(id)

 
def fetchIndividual():
    ##check if it's an ID

    input() # clear the other inputs
    userInput = input('Enter a player ID or gamertag\n')
    fetchIndividualWithID(userInput)
   

