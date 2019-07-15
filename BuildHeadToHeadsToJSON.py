import requests
import json
import importlib

from SQLconnector import connectToSource
from SQLHelper import getTop5PlayersRoster
from ConfigHelper import getConfig

config = getConfig()



def buildHeadToHeads ():
	query = """
with data as ( 
	select p.PlayerID, GamerTag, GameName, GameTimestamp, Score, count(p.PlayerID) over (partition by GameTimestamp order by GameTimestamp desc) countofPlayers, CONVERT(varchar(7),gameTimestamp,25) as gameMonth

	from Participation p 
	join games g on p.GameUUID = g.GameUUID 
	join players pl on pl.PlayerID = p.PlayerID

	where GameName in ('Individual', 'Colour Ranked', 'Highlander','Individual Supercharge','Gladiator (Individual)','Shadows (Individual)')
	and ArenaName = ?
)
	select top(7) d1.PlayerID, d1.Score, d1.GamerTag,  d2.PlayerID, d2.GamerTag, d2.Score,  d1.GameName, convert(varchar(20),d1.GameTimestamp,106) as GT, d1.gameMonth
	from data d1 join data d2 on d1.GameTimestamp = d2.GameTimestamp and d1.PlayerID != d2.PlayerID and d1.Score >= d2.Score
	where d1.countofPlayers = 2 

	order by d1.GameTimestamp desc
	"""


	conn = connectToSource()
	cursor = conn.cursor()

	results = cursor.execute(query,(config["SiteNameReal"]))
	
		
	JSONobject = {"ScoreTitle":"Recent Head to Head games!",
	"Match":[]}
	

	
	
	rows = results.fetchall()
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






