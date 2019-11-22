import json
from psycopg2 import sql
from SQLconnector import connectToSource
import ConfigHelper as cfg
from DBG import DBG
import os
def executeAchievementBuild():
    targetArena = cfg.getConfigString("SiteNameReal")

    query = sql.SQL('''
with PA as (
select  pl.PlayerID, GamerTag,  
	sum ( case when achievedDate is null then 0 when achievedDate is not null then 1 end) as AchievementsCompleted 
	from players pl join PlayerAchievement pa on pl.PlayerID = pa.PlayerID
	join AllAchievements aa on aa.achID = pa.achID
	where aa.ArenaName = %s or aa.ArenaName = 'Global Achievements'
    group by pl.PlayerID, GamerTag, AchievementScore
),
top15 as (
	select * 
	from PA 
	order by AchievementsCompleted desc
	limit 15
),
CountOfAcqusitions as (
	select count(*) acCount, min(pa.achievedDate) earliest, pa.AchID, aa.AchName from 
	PlayerAchievement pa join AllAchievements aa on pa.AchID = aa.AchID
	where ArenaName = %s and achievedDate is not null
	group by pa.AchID, aa.AchName
),
acquiredAAwithRarity as (
	select pa.AchID, acCount, earliest, playerID, AchName
	from CountOfAcqusitions coa join PlayerAchievement pa on coa.achID = pa.AchID 
	where achievedDate is not null
),
finalResults as (
	select row_number() over (partition by aa.playerID order by acCount, earliest) rarityIndex,
	AchName,aa.AchID, acCount, top15.playerID 
	from acquiredAAwithRarity aa join top15 on aa.PlayerID = top15.PlayerID
--order by AchievementsCompleted desc, count
)
select top15.PlayerID,GamerTag,AchievementsCompleted,AchName,acCount
from top15 join finalResults on top15.PlayerID = finalResults.PlayerID
where rarityIndex = 1
order by Achievementscompleted desc
limit 15
    ''')
    data = (targetArena,targetArena)
    conn = connectToSource()
    cursor = conn.cursor()

    cursor.execute(query,data)
    JSON = {
        'ScoreTitle' : "Achievement score & total achievements completed",
        'Player' : [{
        #    'Name' : "C'tri",
        #    'AchievementScore' : -1,
        #    'AchievementsCompleted' : -1,
        }],
        }
    for result in cursor.fetchall():
        #print (result)
        JSON['Player'].append({'Name' : result[1], 'AchievementsCompleted' : result[2], 'RarestAchievement' : result[3], 'OthersWith' : "(%i)" % (result[4])})

    filepart = "Achievements"
    if os.name == "nt":
        divider = "\\" 
    elif os.name == "posix":
        divider = "/"
    f = open("JSONBlobs%s%s%s.json" % (divider, cfg.getConfigString("ID Prefix"),filepart), "w+")
    f.write(json.dumps(JSON,indent=4))
    DBG("Achievement score blob written!",3)


