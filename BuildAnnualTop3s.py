from SQLconnector import connectToSource
import json
conn = connectToSource()
cursor = conn.cursor()

sqlfile = open("/home/ctri/github/LF-Profiler/SQL Queries/PlayerQuality-Big5-allYearByMonth.sql")
SQL = sqlfile.read()#.replace('', '')

conn = connectToSource()
cursor = conn.cursor()

cursor.execute(SQL)
results = cursor.fetchall()
SQLdesc = cursor.description
descCount = 0
for desc in SQLdesc:
    print("%s %s" % (descCount,desc[0]))
    descCount = descCount + 1

currentMonth = ""
months = []
for result in results:
    
    if result [2] != currentMonth:
        currentMonth = result[2]
        print("== New month = [%s]" % (currentMonth,))
        month = {}
        months.append(month)
        month["month"] = result[2]
        players = []
        month["players"] = players
        
    #print(result)
    player = {}
    player["playerName"] = result[4]
    player["gamePlayed"] = result[6]
    player["averageStars"] = "%s" % (result[8])
    players.append(player)
    playerName = "%s%s" % (result[4]," "*15)
    playerName = playerName[0:10]
    print("%s %s, %s games played \t %s stars per game (avg) " % (result[1],playerName , result[6], result[8]) )

print(json.dumps(months,indent=4))
#playerID, rank, month, 
#ID, gamertag, avgopponents
#gamesplayed, averagerank, avgqual
#totalqual, avgscore, achievementscore
#gamemonth
