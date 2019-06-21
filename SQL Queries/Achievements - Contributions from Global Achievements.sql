with data as (select a.PlayerID,p.GamerTag, sum (case 
when achievedDate is not null then 1000 
when progressB is not null then progressB
end) as CalculatedScore, p.AchievementScore
from PlayerAchievement a join Players p on a.PlayerID = p.PlayerID
group by p.AchievementScore, a.PlayerID, p.GamerTag
)
select * , AchievementScore - CalculatedScore as difference 
from data 
order by difference desc