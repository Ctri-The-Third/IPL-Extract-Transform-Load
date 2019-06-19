/****** Script for SelectTopNRows command from SSMS  ******/

SELECT 
	Participation.PlayerID, 
	GamerTag, 
	avg(Score) as averageScore,
	count(GamerTag) as gamesPlayed
  FROM [LaserScraper].[dbo].[Participation]
  inner join Players on Participation.PlayerID = Players.PlayerID
  inner join Games on Participation.GameUUID = Games.GameUUID

  where Games.GameTimestamp >= '2019-05-23' AND 
  Games.GameTimestamp < '2019-06-23'
  and Games.GameName in ('2 Teams','3 Teams','4 Teams', 'Colour Ranked','Individual')
  
  GROUP BY Participation.PlayerID, Players.GamerTag
  order by 3 desc
  
  





