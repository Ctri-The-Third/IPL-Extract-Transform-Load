import json

from SQLconnector import connectToSource
import ConfigHelper as cfg


def executeMonthlyScoresBuild():
  
  startDate = cfg.getConfigString("StartDate")
  endDate = cfg.getConfigString("EndDate")
  LastMonthStart = cfg.getConfigString("LastMonthStart")
  arenaName = cfg.getConfigString("SiteNameReal")
  SQL = '''
  declare @curMonth as varchar(7)
  declare @lastMonth as varchar(7)
  declare @arenaName as varchar(50)
  set @curMonth = ?
  set @lastMonth = ?
  set @arenaName = ?;

	
  with data as  ( select 
	p.PlayerID, 
	GamerTag, 
	avg(Score) as averageScore,
	count(GamerTag) as gamesPlayed,
	convert(varchar(7),GameTimestamp,126) as GameMonth
	
  FROM Participation p
  inner join Players pl on p.PlayerID = pl.PlayerID
  inner join Games g on p.GameUUID = g.GameUUID
  where convert(varchar(7),GameTimestamp,126) in (@curMonth,@lastMonth)
  and (g.GameName in ('Team','3 Teams','4 Teams', 'Colour Ranked','Individual') or
   g.GameName in ('Continous Ind','Standard 2 Team','Standard 3 Team','Standard 4 Team','Standard Individual','Standard Multi team' )
  )
  and g.ArenaName = @arenaName
  GROUP BY p.PlayerID, pl.GamerTag, convert(varchar(7),GameTimestamp,126)
)
  
select d1.PlayerID, d1.GamerTag, d1.averageScore,d1.gamesPlayed, d1.averageScore -d2.averageScore as changeInScore 
from data d1 left join data d2 on d1.PlayerID = d2.PlayerID and d1.GameMonth != d2.GameMonth
where d1.GameMonth = @curMonth	
order by averageScore desc;
  '''
  conn = connectToSource()
  cursor = conn.cursor()

  cursor.execute(SQL,(startDate,LastMonthStart,arenaName))
  JSON = {
      'ScoreTitle' : "Average Scores for known players, in Standard Games, between {1} and {0}" .format(startDate,endDate),
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
      changeInScore = None
      if result[4] is not None: changeInScore = "↑%s" % result[4]  if result[4] > 0 else "↓%s" % abs(result[4])

      JSON['Player'].append({'Name' : result[1], 'AverageScore' : result[2], 'MissionsPlayed' : result[3], "ChangeInScore": changeInScore})

  f = open("JSONBlobs\\MonthlyScoreLatest.json", "w+")
  f.write(json.dumps(JSON,indent=4))
  f = open("JSONBlobs\\%sMonthlyScore.json" % (cfg.getConfigString("ID Prefix")), "w+")
  f.write(json.dumps(JSON,indent=4))
  print ("Monthly average score blobs written!")

