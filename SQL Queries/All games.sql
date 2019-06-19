/****** Script for SelectTopNRows command from SSMS  ******/
SELECT 
	Participation.PlayerID, 
	GamerTag, 
	GameTimestamp, 
	GameName,
    Score
  FROM [LaserScraper].[dbo].[Participation]
  inner join Players on Participation.PlayerID = Players.PlayerID
  inner join Games on Participation.GameUUID = Games.GameUUID
  where GamerTag like '%Para%'
  Order by GameTimestamp desc;





