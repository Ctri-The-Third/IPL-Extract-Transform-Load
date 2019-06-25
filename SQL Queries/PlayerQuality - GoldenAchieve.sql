DECLARE @TargetID as Varchar(10)
SET @TargetID = '7-8-1196';


with firstEarned as (
select distinct min (achievedDate) over (partition by Image) as firstAchieved, Image
from PlayerAchievement
where achievedDate is not null

),
data as ( select count(*) playersEarned,  pa.image, achName from PlayerAchievement pa join AllAchievements aa on pa.Image = aa.image
where achievedDate is not null
group by AchName, pa.Image) 

select top(10) PlayerID, data.AchName, Description, fe.firstAchieved, playersEarned from PlayerAchievement pa 
join data on data.Image = pa.Image
join firstEarned fe on fe.Image = data.Image
join AllAchievements aa on pa.Image = aa.image
where PlayerID = @TargetID
order by playersEarned asc, firstAchieved asc


