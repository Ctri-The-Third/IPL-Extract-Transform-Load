from DBG import DBG
import math
import ConfigHelper as cfg
import SQLHelper
import colorama
from colorama import Fore, Back
import feedbackQueue
#: last 5 games' stats
#: Blobs, month to month.
#: Top achievement in terms of rarity
#: most recent achievements
#: Places visited 
conn = SQLHelper.connectToSource()
cursor = conn.cursor()

colorama.init()

#https://codegolf.stackexchange.com/questions/4707/outputting-ordinal-numbers-1st-2nd-3rd#answer-4712
ordinal = ['0th','%s%s1st%s%s' % (Fore.BLACK,Back.YELLOW,Fore.YELLOW,Back.BLACK), '%s%s2nd%s%s' % (Fore.BLACK,Back.WHITE,Fore.YELLOW,Back.BLACK), '%s%s3rd%s%s' % (Fore.BLACK,Back.RED,Fore.YELLOW,Back.BLACK), '4th', '5th', '6th', '7th', '8th', '9th', '10th',
 '11th', '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th',
 '20th', '21st', '22nd', '23rd', '24th', '25th', '26th', '27th', '28th',
 '29th', '30th', '31st','32nd','33rd','34th','35th','36th','37th','38th','39th','40th','41st','42nd','43rd','44th','45th','46th','47th','48th','49th','50th']



def placesVisited (targetID):
    sql = '''

select  count (*) as gamesPlayed, TO_CHAR (max(g.GameTimestamp),'DD Mon YYYY') as mostRecentVisit, ArenaName from Participation p join Games g on p.GameUUID = g.GameUUID
where p.playerID = %s and ArenaName != %s 
group by ArenaName
order by max(g.GameTimestamp) desc 
limit 1'''
    global cursor
    
    results = cursor.execute(sql,(targetID,cfg.getConfigString("SiteNameReal")))
    feedbackQueue.q.put( "%s%s**Recent travels:**%s\n" % (Back.BLACK,Fore.WHITE,Fore.WHITE))
    for result in cursor.fetchall():
        feedbackQueue.q.put( "%s%s(%svisited %s, on %s. %i observed games played there. %s)%s," % (Back.BLACK,Fore.WHITE,Fore.YELLOW,result[2], result [1], result[0], Fore.WHITE,Fore.WHITE))
    
def recentAchievement (targetID):
    sql = '''DECLARE @targetID  as varchar (20) 
DECLARE @ArenaName as varchar(50)
set @targetID = ?
set @ArenaName = ?;

select top (1) *
from PlayerAchievement pa join AllAchievements aa on pa.Image = aa.image
where PlayerID = @targetID
order by achievedDate desc '''

def rarestAchievement (targetID):
    sql = '''DECLARE @targetID  as varchar (20) 
DECLARE @ArenaName as varchar(50)
set @targetID = ?;
set @ArenaName = ?;

with bigData as (
select aa.image, AchName, count (distinct PlayerID) as achievingPlayers
from PlayerAchievement pa join AllAchievements aa on pa.Image = aa.image
where pa.achievedDate is not null and ArenaName = @ArenaName
group by aa.image, AchName
)
select top (1) *
from PlayerAchievement pa join bigData bd on pa.Image = bd.image
where PlayerID = @targetID
order by achievingPlayers asc, achievedDate asc'''


def blobs (targetID):
    sql = '''
with Ranks as 
(
	select GameTimestamp,games.GameUUID, GameName, Players.PlayerID, GamerTag, Score, 
		ROW_NUMBER() over (partition by GameTimestamp order by score desc) as gamePosition
	from Games 
	join Participation on Games.GameUUID = Participation.GameUUID
	join Players on Participation.PlayerID = Players.PlayerID
	where Games.ArenaName = %s
),
totalPlayersPerGame as 
(
	select g.GameUUID, count(*) as playerCount
	from Participation p join Games g on p.GameUUID = g.GameUUID
	group by g.GameUUID
)
, starData0 as  (
select to_char(gametimestamp, 'YYYY-MM') as month
, ranks.GameUUID,GameTimestamp
, GameName
, PlayerID,GamerTag
, gamePosition
, playerCount
from ranks join totalPlayersPerGame tppg 
on ranks.GameUUID = tppg.GameUUID
)
,starData1 as (
	select month
	, PlayerID,count(*) games
	, round(avg(cast(gamePosition as numeric)),2) avgRank
	, round(avg(cast(playercount as numeric)),2) avgOpponents
	, round(avg(cast(playercount as numeric))  * (avg(cast(playercount as numeric)) / avg(cast(gamePosition as numeric))),2) as avgSQ
	from starData0 
	group by  month, PlayerID
)
, starData2 as (
	select ROW_NUMBER() over (partition by month order by month desc, avgSQ desc) SQrank, * from starData1
)
, StdData0 as( select 
	p.PlayerID, 
	GamerTag, 
	avg(Score) as averageScore,
	count(GamerTag) as gamesPlayed,
	to_char(GameTimestamp, 'YYYY-MM') as GameMonth	
  FROM Participation p
  inner join Players pl on p.PlayerID = pl.PlayerID
  inner join Games g on p.GameUUID = g.GameUUID
  --where convert(varchar(7),GameTimestamp,126) in (@curMonth,@lastMonth)
  and (g.GameName in ('Team','3 Teams','4 Teams', 'Colour Ranked','Individual') or
   g.GameName in ('Continous Ind','Standard 2 Team','Standard 3 Team','Standard 4 Team','Standard Individual','Standard Multi team' )
  )
  and g.ArenaName = %s
  GROUP BY p.PlayerID, pl.GamerTag, to_char(GameTimestamp, 'YYYY-MM')
)
, stdData1 as (
  select *, ROW_NUMBER() over (partition by GameMonth order by averageScore desc) as stdRank from StdData0
)
 -- players * (players/rank)
select month,SQrank,avgSQ,games,stdRank,averageScore,gamesPlayed
from starData2 sq
join StdData1 sd on sq.PlayerID = sd.PlayerID and sq.month = sd.GameMonth
where sq.PlayerID = %s 
order by month desc 
limit 3
'''
    global cursor
    global config
    global ordinal
    data = (targetID,cfg.getConfigString("SiteNameReal"),targetID)
    cursor.execute(sql,data)
    feedbackQueue.q.put( "%s%s**Month to Month Stats:**%s\n" % (Back.BLACK,Fore.WHITE,Fore.WHITE))
    for result in cursor.fetchall():
        #print(result)
        if int(result[4]) > 50 or int(result[4]) < 0:
            ordinalString = result[4]
        else : 
            ordinalString = ordinal[int(result[4])]

        temptStr = "%s: Stars %s (%s)\t Std %s (%s)" % (result[0],ordinal[int(result[1])],result[2],ordinalString,result[5])
        feedbackQueue.q.put( "%s%s(%s%s%s)%s\n" % (Back.BLACK,Fore.WHITE,Fore.YELLOW,temptStr,Fore.WHITE,Fore.WHITE))


def recentGames(targetID):
    sql = '''
with Ranks as 
(
	select GameTimestamp,games.GameUUID, GameName, Players.PlayerID, GamerTag, Score, 
		ROW_NUMBER() over (partition by GameTimestamp order by score desc) as gamePosition
	from Games 
	join Participation on Games.GameUUID = Participation.GameUUID
	join Players on Participation.PlayerID = Players.PlayerID
	where Games.ArenaName = %s
),
totalPlayersPerGame as 
(
	select g.GameUUID, count(*) as playerCount
	from Participation p join Games g on p.GameUUID = g.GameUUID
	group by g.GameUUID
)
select ranks.GameUUID
	,to_char(GameTimestamp,'DD Mon YYYY')
	,GameName
	,PlayerID
	,GamerTag
	,gamePosition
	,playerCount
	,playerCount  * ( playerCount  / gamePosition ) as SQ
from ranks join totalPlayersPerGame tppg 
on ranks.GameUUID = tppg.GameUUID
where PlayerID = %s
order by GameTimestamp desc
limit 3 
    '''
    global ordinal
    global cursor
    global config
    cursor.execute(sql,(targetID,cfg.getConfigString("SiteNameReal")))
    results = cursor.fetchall()
    feedbackQueue.q.put("%s%s**Recent Games: for %s at %s **%s\n" % (Back.BLACK,Fore.WHITE,targetID,cfg.getConfigString("SiteNameShort"),Fore.WHITE))
    for result in results:
        #print(result)
        temptStr = "%s: %s       rank %s, of %s" % (result[1],(result[2]+" "*15)[:15],ordinal[int(result[5])],result[6])
        feedbackQueue.q.put( "%s%s(%s%s%s)%s\n" % (Back.BLACK,Fore.WHITE,Fore.YELLOW,temptStr,Fore.WHITE,Fore.WHITE))


def PlaysWhen(targetID):
    sql = '''
with dateData as (
select distinct case 
	when EXTRACT(DOW FROM GameTimestamp) = 1 then 'Sunday'
	when EXTRACT(DOW FROM GameTimestamp) = 2 then 'Monday'
	when EXTRACT(DOW FROM GameTimestamp) = 3 then 'Tuesday'
	when EXTRACT(DOW FROM GameTimestamp) = 4 then 'Wednesday'
	when EXTRACT(DOW FROM GameTimestamp) = 5 then 'Thursday'
	when EXTRACT(DOW FROM GameTimestamp) = 6 then 'Friday'
	when EXTRACT(DOW FROM GameTimestamp) = 7 then 'Saturday'
end as dayName, 
	EXTRACT(DOW FROM GameTimestamp) as day
from Games
),
data as (
	select count (*) as games, EXTRACT(DOW FROM GameTimestamp) as day, EXTRACT(hour FROM GameTimestamp) as hour
	from players pl join Participation p on pl.PlayerID = p.PlayerID 
	join games g on p.GameUUID = g.GameUUID
	where p.playerID = %s
	and g.ArenaName = %s
	group by day, hour
)
select games,dayName,hour from data d join   dateData dd on d.day =dd.day
order by games desc
limit 2
'''
    global ordinal
    global cursor
    global config
    data =(targetID,cfg.getConfigString("SiteNameReal"))
    cursor.execute(sql,data)
    feedbackQueue.q.put( "%s%s**Common Game Times:**%s\n" % (Back.BLACK,Fore.WHITE,Fore.WHITE))
    for result in cursor.fetchall():
        #print(result)
        temptStr = "on %s at %s:00ish" % (result[1],result[2])
        feedbackQueue.q.put( "%s%s(%s%s%s)%s," % (Back.BLACK,Fore.WHITE,Fore.YELLOW,temptStr,Fore.WHITE,Fore.WHITE))
    

def findPlayer(targetID):
    global cursor
    if cursor == None:
        cursor = SQLHelper.connectToSource().cursor()
    exactMatch = """select PlayerID from Players where playerID = %s limit 1"""
    cursor.execute(exactMatch,(targetID,))
    result = cursor.fetchall()

    if result == None or len(result) == 0:
        localID = cfg.getConfigString("ID Prefix") + targetID 
        cursor.execute(exactMatch,(localID,))
        cursor.fetchall()
        if result != None and len(result) == 1:
            return result[0][0]

    else: 
        return targetID
        
    nameMatch = """select top PlayerID, Missions
        from players 
        where GamerTag like %s
        order by missions desc
        limit 1 
        """
    name = '%%%s%%' % targetID
    cursor.execute(nameMatch,(name,))
    results = cursor.fetchone()
    if result != None and len(result) == 1:
        return result[0][0]
    return "0-0-0"
    #Check prefix+suffix
    #check for 'like', and retrieve player with most missions in current arena

def executeQueryIndividual (initTargetID):
    targetID = findPlayer(initTargetID)
    if targetID == "0-0-0":
        DBG("Unable to find a player with ID or name [%s]" % initTargetID, 2)
        return
    recentGames(targetID) 
    blobs(targetID)
    PlaysWhen(targetID)
    rarestAchievement(targetID)
    recentAchievement(targetID)
    placesVisited(targetID)
    