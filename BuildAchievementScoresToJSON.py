import json

from SQLconnector import connectToSource


def executeAchievementBuild():
    SQL = '''
    select TOP (15) players.PlayerID, GamerTag, AchievementScore, sum ( case when achievedDate is null then 0 when achievedDate is not null then 1 end) as AchievementsCompleted from players
    join PlayerAchievement on Players.PlayerID = PlayerAchievement.PlayerID
    group by players.PlayerID, GamerTag, AchievementScore
    order by AchievementScore desc

    '''
    conn = connectToSource()
    cursor = conn.cursor()

    cursor.execute(SQL)
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
        JSON['Player'].append({'Name' : result[1], 'AchievementScore' : result[2], 'AchievementsCompleted' : result[3]})

    f = open("JSONBlobs\\AchievementsLatest.json", "w+")
    f.write(json.dumps(JSON,indent=4))
    print ("Achievement score blob written!")