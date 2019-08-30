import json

from SQLconnector import connectToSource
import ConfigHelper as cfg

def executeAchievementBuild():
    targetArena = cfg.getConfigString("SiteNameReal")

    SQL = '''
declare @arenaName as varchar(50)
set @arenaName = ?;
with PA as (
select  pl.PlayerID, GamerTag,  
	sum ( case when achievedDate is null then 0 when achievedDate is not null then 1 end) as AchievementsCompleted 
	from players pl join PlayerAchievement pa on pl.PlayerID = pa.PlayerID
	join AllAchievements aa on aa.achID = pa.achID
	where aa.ArenaName =@arenaName or aa.ArenaName = 'Global Achievements'
    group by pl.PlayerID, GamerTag, AchievementScore
),
top15 as (
	select top(15) * from PA 
	order by AchievementsCompleted desc
),
CountOfAcqusitions as (
	select count(*) count, min(pa.achievedDate) earliest, pa.AchID, aa.AchName from 
	PlayerAchievement pa join AllAchievements aa on pa.AchID = aa.AchID
	where ArenaName = @arenaName and achievedDate is not null
	group by pa.AchID, aa.AchName

),
acquiredAAwithRarity as (
	select pa.AchID, count, earliest, playerID, AchName
	from CountOfAcqusitions coa join PlayerAchievement pa on coa.achID = pa.AchID 
	where achievedDate is not null
),
finalResults as (
	select row_number() over (partition by aa.playerID order by count, earliest) rarityIndex,
	AchName,aa.AchID, count, top15.playerID 
	from acquiredAAwithRarity aa join top15 on aa.PlayerID = top15.PlayerID
--order by AchievementsCompleted desc, count
)


select top (15)  top15.PlayerID,GamerTag,AchievementsCompleted,AchName,count
from top15 join finalResults on top15.PlayerID = finalResults.PlayerID
where rarityIndex = 1
order by Achievementscompleted desc



    '''
    conn = connectToSource()
    cursor = conn.cursor()

    cursor.execute(SQL,(targetArena))
    JSON = {
        'ScoreTitle' : "Achievement score & total achievements completed",
        'Player' : [{
        #    'Name' : "C'tri",
        #    'AchievementScore' : -1,
        #    'AchievementsCompleted' : -1,
        }],
        }
    for result in cursor.fetchall():
        print (result)
        JSON['Player'].append({'Name' : result[1], 'AchievementsCompleted' : result[2], 'RarestAchievement' : result[3], 'OthersWith' : "(%i)" % (result[4])})

    
    f = open("JSONBlobs\\%sAchievements.json" % (cfg.getConfigString("ID Prefix")), "w+")
    f.write(json.dumps(JSON,indent=4))
    print ("Achievement score blob written!")


