import pyodbc
from SQLconnector import connectToSource
from FetchPlayerUpdatesAndNewPlayers import manualTargetSummary
from FetchPlayerAndGames import manualTargetForGames
from FetchAchievements import manualTargetAchievements
conn = connectToSource()
cursor = conn.cursor()

userInput = input('Enter a player ID or gamertag\n')

SQL = """select * from Players where PlayerID = ?"""
cursor.execute(SQL,(userInput))
results = cursor.fetchall()

if len(results) == 1:
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

else: 
    userInput = "%" + userInput + "%"
    print("Didn't find player ID, searching for gamertag")
    SQL = """select PlayerID, Gamertag, Missions from Players where GamerTag like ?"""
    cursor.execute(SQL,(userInput))
    
    results = cursor.fetchall()
    for player in results:
        print ("Found player %s, gamerTag = %s, missions = %i" % (player[0], player[1], player[2]))