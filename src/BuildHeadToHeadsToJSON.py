import requests
import json
import importlib

from SQLconnector import connectToSource
from SQLHelper import getTop5PlayersRoster
import ConfigHelper as cfg





def buildHeadToHeads ():
	query = """
with data as ( 
	select p.PlayerID
	, GamerTag
	, GameName
	, GameTimestamp
	, Score
	, count(p.PlayerID) over (partition by GameTimestamp order by GameTimestamp desc) countofPlayers
	, TO_CHAR(gameTimestamp,'YYYY-MM') as gameMonth
	from Participation p 
	join games g on p.GameUUID = g.GameUUID 
	join players pl on pl.PlayerID = p.PlayerID
	where GameName in ('Individual', 'Colour Ranked', 'Highlander','Individual Supercharge','Gladiator (Individual)','Shadows (Individual)')
	and ArenaName = %s
)
select d1.PlayerID, d1.Score, d1.GamerTag,  d2.PlayerID, d2.GamerTag, d2.Score,  d1.GameName, to_char(d1.GameTimestamp,'DD Mon YYYY') as GT, d1.gameMonth
from data d1 join data d2 on d1.GameTimestamp = d2.GameTimestamp and d1.PlayerID != d2.PlayerID and d1.Score >= d2.Score
where d1.countofPlayers = 2 
order by d1.GameTimestamp desc
limit 7"""

	data = (cfg.getConfigString("SiteNameReal"),)
	conn = connectToSource()
	cursor = conn.cursor()

	results = cursor.execute(query,data)
	
		
	JSONobject = {"ScoreTitle":"Recent Head to Head games!",
	"Match":[]}
	

	
	
	rows = cursor.fetchall()
	for row in rows:
		JSONobject["Match"].append(
			{"Player1Name":row[2],
			"Player1Score":row[1],
			"Player2Name":row[4],
			"Player2Score":row[5],
			"GameDate":row[7]})
		print(row)

	f = open("JSONBlobs\\HeadToHeads.json", "w+")
	f.write(json.dumps(JSONobject,indent=4))
	f.close()
	print("Head to Head matches written!")






