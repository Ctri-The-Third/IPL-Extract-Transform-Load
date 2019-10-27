"""This module will do a check on the DB every heartbeat, and check for jobs that are more than 4 heartbeats old.
On finding such, it will attempt to restart the job."""
import time
import json
import FetchPlayerAndGames
import FetchPlayerUpdatesAndNewPlayers
import threading
from  SQLconnector import connectToSource

 
__terminateInstruction__ = False
def startMonitorThreads():
    thread = threading.Thread(target=executeMonitor)
    thread.start()
    return thread

def executeMonitor():
    conn = connectToSource()
    cursor = conn.cursor()
    SQL = """with data as (
                select EXTRACT(EPOCH  from (now() - COALESCE (lastheartbeat, started))) as age, *
                from jobslist 
                
            )
            select * from data
            where finished is null and age > 120 
            order by lastheartbeat asc, started asc
 """
    seconds = 0
    while not isTerminated():
        seconds = seconds + 1
        if seconds % 30 == 0: #every 30th second
            seconds = 0
            cursor.execute(SQL)
            conn.commit()
            #print ("---")
            for result in cursor.fetchall():
                if result[3] == "FetchPlayerAndGames.executeQueryGames":
                    params = json.loads(result[8])
                    t = threading.Thread(
                        target=FetchPlayerAndGames.executeQueryGames, 
                        args=(params["scope"],), 
                        kwargs={"ID":result[2],"offset":result[7]}) #
                    t.start()
                if result[3] == "FetchPlayerUpdatesAndNewPlayers.updateExistingPlayers":
                    t = threading.Thread(
                        target=FetchPlayerUpdatesAndNewPlayers.updateExistingPlayers, 
                        #args=(params["scope"],), 
                        kwargs={"JobID":result[2]}) #this method gets offset from the job ID
                    t.start()
                    #execute known method.
                print(result)
        time.sleep(1)

def terminateMonitor():
    global __terminateInstruction__
    __terminateInstruction__ = True
    return

def isTerminated():
    global __terminateInstruction__
    return __terminateInstruction__
