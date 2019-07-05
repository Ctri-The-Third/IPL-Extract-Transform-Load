/****** Script for SelectTopNRows command from SSMS  ******/
SELECT 
	Participation.PlayerID as PID, 
	GamerTag, 
	GameTimestamp, 
	GameName,
    Score
  FROM [LaserScraper].[dbo].[Participation]
  inner join Players on Participation.PlayerID = Players.PlayerID
  inner join Games on Participation.GameUUID = Games.GameUUID
  where GamerTag in ('Youtube Candle', 'Deadpool')
  Order by GameTimestamp desc;







