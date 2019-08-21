import pyodbc  
import re
from SQLconnector import connectToSource
from FetchPlayerUpdatesAndNewPlayers import manualTargetSummary
from FetchPlayerAndGames import manualTargetForGames
from FetchAchievements import manualTargetAchievements





def fetchIndividual():
    ##check if it's an ID
    conn = connectToSource()
    cursor = conn.cursor()
    input() # clear the other inputs
    userInput = input('Enter a player ID or gamertag\n')
    if re.match("([0-9]+)-([0-9]+)-([0-9]+)",userInput):

        SQL = """select * from Players where PlayerID = ?"""
        cursor.execute(SQL,(userInput))
        results = cursor.fetchall()

        if len(results) >= 1:
            print(results)
            print("Fount player, updating")
            manualTargetSummary(userInput)
            manualTargetForGames(userInput)
            manualTargetAchievements(userInput)
            
            from BuildAchievementScoresToJSON import executeAchievementBuild
            from BuildHeadToHeadsToJSON import buildHeadToHeads
            from BuildMonthlyScoresToJSON import executeMonthlyScoresBuild
            from BuildPlayerBlob import executeBuildPlayerBlobs
            from BuildMonthlyStarQualityToJSON import executeBuildMonthlyStars
            executeAchievementBuild()
            executeMonthlyScoresBuild()
            buildHeadToHeads()
            executeBuildPlayerBlobs()
            executeBuildMonthlyStars()
        elif len(results) == 0:
            print("Didn't find ID in database, performing summary search")
            manualTargetSummary(userInput)
    else: 
        userInput = "%" + userInput + "%"
        print("Didn't find player ID, searching for gamertag")
        SQL = """select PlayerID, Gamertag, Missions from Players where GamerTag like ?"""
        cursor.execute(SQL,(userInput))
        
        results = cursor.fetchall()
        for player in results:
            print ("Found player %s, gamerTag = %s, missions = %i" % (player[0], player[1], player[2]))
