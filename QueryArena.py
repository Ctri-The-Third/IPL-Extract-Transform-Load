from DBG import DBG
import math
import ConfigHelper as cfg
import SQLHelper
import colorama
from colorama import Fore, Back
import feedbackQueue
from psycopg2 import sql

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

config = {}

SQLplayerKPIs = """
declare @startDate as varchar(10) 
declare @endDate as varchar(10) 
declare @targetArena as varchar(50)
set @targetArena = 'Funstation Ltd, Edinburgh, Scotland';

with uniquePlayerData as (
	select convert(varchar(7),g.GameTimestamp,126)  month, count(distinct PlayerID) players, ROW_NUMBER() over ( order by convert(varchar(7),g.GameTimestamp,126)  desc) row
	from Participation p join games g 
	on p.GameUUID = g.GameUUID
	where g.ArenaName = @targetArena
	group by convert(varchar(7),g.GameTimestamp,126)
),
participationData as (
	select convert(varchar(7),g.GameTimestamp,126)  month, count(*) participations, ROW_NUMBER() over ( order by convert(varchar(7),g.GameTimestamp,126)  desc) row
	from Participation p join games g 
	on p.GameUUID = g.GameUUID
	where g.ArenaName = @targetArena
	group by convert(varchar(7),g.GameTimestamp,126)
)
select d1.month,d1.players, d1.players - d2.players as change, pd.participations, pd.participations - pd2.participations as change
from uniquePlayerData d1 left join uniquePlayerData d2 on d1.row = d2.row-1
join participationData pd on d1.month = pd.month 
left join participationData pd2 on pd.row = pd2.row - 1 
"""
SQLdataRecency = """
DO $$
declare @targetArena as varchar(50)
set @targetArena = 'Funstation Ltd, Edinburgh, Scotland';

with data as (
select max(g.GameTimestamp) latestGame, CURRENT_TIMESTAMP now
from games g
where ArenaName = @targetArena)
select convert(varchar(16),latestGame,120) mostRecentGame, Datediff (hour,latestGame,CURRENT_TIMESTAMP) as lag from data """

SQLnewAndLostPlayers = """
declare @startDate as varchar(10) 
declare @endDate as varchar(10) 
declare @lastMonth as varchar(10) 
declare @targetArena as varchar(50)
set @targetArena = 'Funstation Ltd, Edinburgh, Scotland'
set @startDate = '2019-07-01'
set @endDate = '2019-08-01'
set @lastMonth = '2019-06-01';
with data as (
select count(*) missions, min(g.gameTimestamp) firstSeen, max(g.gameTimestamp) lastSeen, p.playerID, pl.GamerTag
from Participation p join Games G on p.GameUUID = g.GameUUID
join players pl on p.PlayerID = pl.PlayerID
where g.ArenaName = @targetArena
group by p.PlayerID, pl.GamerTag
), churnedPlayers as (
	select count(*) as churnedPlayers from data where 
	lastSeen > @lastMonth and lastSeen < @startDate
), newPlayers as (
	select count(*) as newPlayers from data where 
	firstSeen >= @startDate and firstSeen <= @endDate
)
select * from churnedPlayers cp full outer join newPlayers np on 1=1
"""

def executeQueryArena (initTargetID):
    global config 

    
    config = cfg.getConfig() #cache the config
    # Note, a "Member" is someone who is level 4 or higher, or has played more than 15 games.
    #Number of distinct players this month, last month, & change - SQLplayerKPIs
    #Number of distinct participations this month - SQLplayerKPIs
    #Month on Month change - SQLplayerKPIs
    #LastGame detected (Yellow if over 2 days, RED if more than 5) - SQLdataRecency
    #PlayerVeterancy by weeks (0,1,2,3,4,8,12, 26, 52)
    #NewMembersDetected - SQLnewAndLostPlayers
    #ChurnedMembers (60 days)




executeQueryArenaName = ""
executeQueryArenaValue = ""

def healthCheck (arenaName):
    global executeQueryArenaName 
    global executeQueryArenaValue
    if executeQueryArenaName == arenaName:
        return executeQueryArenaValue
        
    
    SQLdataRecency = sql.SQL("""
with data as (
select max(g.GameTimestamp) latestGame, CURRENT_TIMESTAMP now
from games g
where ArenaName = %s)
select to_char(latestGame,'YYYY-MM-DD HH24:MI') mostRecentGame, DATE_PART('day', NOW() - latestGame)
 * 24 + DATE_PART('hour', NOW() - latestGame ) as lag
 from data 
 """)
    global conn
    cursor = conn.cursor()
    cursor.execute(SQLdataRecency, (arenaName,))
    row = cursor.fetchone()
    if row[1] > 120:
        cacheTarget = arenaName
        cacheResponse = 2
        return 2
    elif row[1] > 48:
        cacheTarget = arenaName
        cacheResponse = 1
        return 1
    else:
        cacheTarget = arenaName
        cacheResponse = 0
        return 0


