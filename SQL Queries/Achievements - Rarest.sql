with data as ( select top (10) count (PlayerID) playersWith, a.image, min(achievedDate) as firstAchieved
from PlayerAchievement pa join AllAchievements a on pa.Image = a.Image
where pa.achievedDate is not null
and a.Description is not null
group by  a.image
order by playersWith asc, firstAchieved asc

)

select playersWith,AchName,Description, data.image
from data join AllAchievements a on data.image = a.image
order by playersWith asc, firstAchieved asc