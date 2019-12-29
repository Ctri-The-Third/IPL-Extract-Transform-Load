from SQLconnector import connectToSource

conn = connectToSource()
cursor = conn.cursor()

sqlfile = open("/home/ctri/github/LF-Profiler/SQL Queries/PlayerQuality-Big5-allYearByMonth.sql")
SQL = sqlfile.read()#.replace('', '')

conn = connectToSource()
cursor = conn.cursor()

cursor.execute(SQL)
results = cursor.fetchall()
SQLdesc = cursor.description
for desc in SQLdesc:
    print(desc[0])

currentMonth = ""
months = []
for result in results:
    print(result)
    if result [2] != currentMonth:

#playerID, rank, month, 
#ID, gamertag, avgopponents
#gamesplayed, averagerank, avgqual
#totalqual, avgscore, achievementscore
#gamemonth

