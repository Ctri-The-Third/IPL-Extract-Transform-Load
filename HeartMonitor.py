"""This module will do a check on the DB every heartbeat, and check for jobs that are more than 4 heartbeats old.
On finding such, it will attempt to restart the job."""
import time
import json
import FetchPlayerAndGames
import FetchPlayerUpdatesAndNewPlayers
import FetchAchievements
import threading
import threadRegistrationQueue as TRQ
from  SQLconnector import connectToSource

 
__terminateInstruction__ = False
def startMonitorThreads():
    thread = threading.Thread(target=executeMonitor)
    thread.name = "HeartMonitor" 
    thread.start()
    return thread

def executeMonitor():
    conn = connectToSource()
    cursor = conn.cursor()
    SQL = """
            select age,"desc",ID,methodname,started,finished,lastheartbeat,resumeindex, methodParams, healthstatus,percenttocompletion 
            from public."jobsView"
            where finished is null and age > 120 
            order by lastheartbeat asc, started asc
 """
    seconds = 0
    while not isTerminated():
        seconds = seconds + 1
        if seconds % 30 == 1: #every 30th second
            seconds = 0
            cursor.execute(SQL)
            conn.commit()
            #print ("---")
            for result in cursor.fetchall():
                if result[3] == "FetchPlayerAndGames.executeQueryGames":
                    params = json.loads(result[8])
                    if result[7] is not None:
                        print("Debug insertion")
                    t = threading.Thread(
                        target=FetchPlayerAndGames.executeQueryGames, 
                        args=(params["scope"],), 
                        kwargs={"ID":result[2],"offset":result[7]}) #
                    t.start()
                    t.name = result[3]
                    TRQ.q.put(t)
                    
                
                elif result[3] == "FetchPlayerUpdatesAndNewPlayers.updateExistingPlayers":
                    t = threading.Thread(
                        target=FetchPlayerUpdatesAndNewPlayers.updateExistingPlayers, 
                        #args=(params["scope"],), 
                        kwargs={"JobID":result[2]}) #this method gets offset from the job ID
                    t.start()
                    t.name = result[3]
                    TRQ.q.put(t)

                    #execute known method.



                elif result[3] == "FetchAchievements.executeFetchAchievements":
                    params = json.loads(result[8])
                    t = threading.Thread(
                        target=FetchAchievements.executeFetchAchievements, 
                        args=(params["scope"],), 
                        kwargs={"jobID":result[2],"offset":result[7]}) #
                    t.start()
                    t.name = result[3]
                    TRQ.q.put(t)



                elif result[3] == "FetchPlayerUpdatesAndNewPlayers.findNewPlayers":
                    params = json.loads(result[8])
                    t = threading.Thread(
                        target=FetchPlayerUpdatesAndNewPlayers.findNewPlayers, 
                        #args=(params["siteName"],), 
                        kwargs={"jobID":result[2],"siteName":params["siteName"]}
                        ) #
                    t.start()
                    t.name = result[3]
                    TRQ.q.put(t)
                
                #print(result)
        time.sleep(1) #sleep for a second to allow termination checks

def terminateMonitor():
    global __terminateInstruction__
    __terminateInstruction__ = True
    return

def isTerminated():
    global __terminateInstruction__
    return __terminateInstruction__


#FetchAchievements.executeFetchAchievements('recent',jobID='7e0b0aec-6a90-4672-ba75-1c676f69cb3c',offset=86)