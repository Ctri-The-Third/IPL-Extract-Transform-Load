import json

from SQLconnector import connectToSource
startDate = '2019-07-01'
endDate = '2019-08-01'
SQL = '''SELECT 
	Participation.PlayerID, 
	GamerTag, 
	avg(Score) as averageScore,
	count(GamerTag) as gamesPlayed
  FROM [LaserScraper].[dbo].[Participation]
  inner join Players on Participation.PlayerID = Players.PlayerID
  inner join Games on Participation.GameUUID = Games.GameUUID

  where Games.GameTimestamp >= ? AND 
  Games.GameTimestamp < ?
  and Games.GameName in ('2 Teams','3 Teams','4 Teams', 'Colour Ranked','Individual')
  
  GROUP BY Participation.PlayerID, Players.GamerTag
  order by 3 desc
'''
conn = connectToSource()
cursor = conn.cursor()

cursor.execute(SQL,(startDate,endDate))
JSON = {
    'ScoreTitle' : "Average Scores for known players, in Standard Games, between {0} and {1}" .format(startDate,endDate),
    'ScoreGreaterOrEqualDate' : startDate,
    'ScoreLessDate' : endDate,
    'Player' : [{
    #    'Name' : "C'tri",
    #    'AverageScore' : -1,
    #    'MissionsPlayed' : -1,
    }],
    }
for result in cursor.fetchall():
    print (result)
    JSON['Player'].append({'Name' : result[1], 'AverageScore' : result[2], 'MissionsPlayed' : result[3]})

f = open("JSONBlobs\\MonthlyScoreLatest.json", "w+")
f.write(json.dumps(JSON))
f = open("JSONBlobs\\MonthlyScore{0}to{1}.json".format(startDate,endDate), "w+")
f.write(json.dumps(JSON))
print ("Monthly average score blobs written!")