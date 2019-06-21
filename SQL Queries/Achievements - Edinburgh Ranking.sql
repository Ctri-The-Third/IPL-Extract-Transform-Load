select players.PlayerID, GamerTag, AchievementScore, count ( case when achievedDate is null then 0 when achievedDate is not null then 1 end) as AchievementsCompleted from players
join PlayerAchievement on Players.PlayerID = PlayerAchievement.PlayerID
group by players.PlayerID, GamerTag, AchievementScore
order by AchievementScore desc