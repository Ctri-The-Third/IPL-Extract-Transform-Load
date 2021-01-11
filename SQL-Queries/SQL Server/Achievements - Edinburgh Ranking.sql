declare @arenaName as varchar(50)
set @arenaName = ''

select 
	players.PlayerID, 
	GamerTag, 
	AchievementScore, 
	AllAchievements.ArenaName,
	sum ( case when achievedDate is null then 0 when achievedDate is not null then 1 end) as AchievementsCompleted 
from players
join PlayerAchievement on Players.PlayerID = PlayerAchievement.PlayerID
join AllAchievements on PlayerAchievement.Image = AllAchievements.image
group by players.PlayerID, GamerTag, AchievementScore, ArenaName
order by PlayerID desc