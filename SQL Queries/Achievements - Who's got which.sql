
with Player1Achievements as (
select Image, PlayerID From PlayerAchievement 
where achievedDate is not null
and PlayerID = '9-6-106'),
Player2Achievements as (
select Image, PlayerID from PlayerAchievement
where achievedDate is not null
and PlayerID = '7-9-126')

select Player1Achievements.PlayerID, a.AchName , Player2Achievements.PlayerID, b.AchName from Player1Achievements full outer join Player2Achievements on
Player1Achievements.Image = Player2Achievements.Image
full outer join AllAchievements a on Player1Achievements.Image = a.image
full outer join AllAchievements b on Player2Achievements.Image = b.image
where (Player1Achievements.PlayerID is null 
OR Player2Achievements.PlayerID is null )
and not (Player1Achievements.PlayerID is null AND Player2Achievements.PlayerID is null)

--select * from players where GamerTag like 'achi%'