import time
import json
import FetchPlayerAndGames
from  SQLconnector import connectToSource

#This module will do a check on the DB every heartbeat, and check for jobs that are more than 4 heartbeats old.
#On finding such, it will attempt to restart the job.
__terminateInstruction__ = False
def executeMonitor():
    conn = connectToSource()
    cursor = conn.cursor()
    while not isTerminated():
        SQL = """with data as (
                select EXTRACT(EPOCH  from (now() - COALESCE (lastheartbeat, started))) as age, *
                from jobslist 
                
            )
            select * from data
            where finished is null and age > 120 
            order by lastheartbeat asc, started asc
 """
        
        cursor.execute(SQL)
        conn.commit()
        print ("---")
        for result in cursor.fetchall():


            if result[3] == "FetchPlayerAndGames.executeQueryGames":
                params = json.loads(result[8])
                FetchPlayerAndGames.executeQueryGames(params["scope"])
                #execute known method.
            print(result)
        time.sleep(120)

def terminateMonitor():
    __terminateInstruction__ = True
    return

def isTerminated():
    return __terminateInstruction__
executeMonitor()