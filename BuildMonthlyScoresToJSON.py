
import os
import json

from SQLconnector import connectToSource
import ConfigHelper as cfg
from DBG import DBG


def executeMonthlyScoresBuild():
  
  startDate = cfg.getConfigString("StartDate")
  endDate = cfg.getConfigString("EndDate")
  LastMonthStart = cfg.getConfigString("LastMonthStart")
  arenaName = cfg.getConfigString("SiteNameReal")
  SQL = '''
with data as  ( 
  SELECT
	p.PlayerID, 
	GamerTag, 
	avg(Score) as averageScore,
	count(GamerTag) as gamesPlayed,
	to_char(GameTimestamp,'YYYY-MM') as GameMonth
	
  FROM Participation p
  inner join Players pl on p.PlayerID = pl.PlayerID
  inner join Games g on p.GameUUID = g.GameUUID
  where to_char(GameTimestamp,'YYYY-MM') in  (%s,%s)

  and (
	g.GameName in ('Team','3 Teams','4 Teams', 'Colour Ranked','Individual')
    or g.GameName in ('Standard - Solo', 'Standard - Team','Standard [3 Team] (10)','Standard [3 Team] (15)','Standard 2 Team',
    'Standard 3 Team','Standard 4 Team','Standard Individual','Standard Multi team','- Standard [2 Team] (15))')
	)
  and g.ArenaName = %s
  GROUP BY p.PlayerID, pl.GamerTag, to_char(GameTimestamp,'YYYY-MM')
)
  
select d1.PlayerID, d1.GamerTag, cast(d1.averageScore as int),d1.gamesPlayed, round(cast(d1.averageScore -d2.averageScore as numeric),2) as changeInScore 
from data d1 left join data d2 on d1.PlayerID = d2.PlayerID and d1.GameMonth != d2.GameMonth
where d1.GameMonth = %s
order by averageScore desc;
  '''
  conn = connectToSource()
  cursor = conn.cursor()

  cursor.execute(SQL,(startDate[0:7],LastMonthStart[0:7],arenaName,startDate[0:7]))
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
      #print (result)
      changeInScore = None
      if result[4] is not None: changeInScore = "↑%s" % result[4]  if result[4] > 0 else "↓%s" % abs(result[4])

      JSON['Player'].append({'Name' : result[1], 'AverageScore' : result[2], 'MissionsPlayed' : result[3], "ChangeInScore": changeInScore})
  filepart = "MonthlyScore"
  if os.name == "nt":
      divider = "\\" 
  elif os.name == "posix":
      divider = "/"
  f = open("JSONBlobs%s%sLatest.json" % (divider,filepart), "w+")
  f.write(json.dumps(JSON,indent=4))
  f = open("JSONBlobs%s%s%s.json" % (divider, cfg.getConfigString("ID Prefix"),filepart), "w+")
  f.write(json.dumps(JSON,indent=4))
  DBG ("Monthly average score blobs written!",3)

