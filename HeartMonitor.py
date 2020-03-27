"""This module will do a check on the DB every heartbeat, and check for jobs that are more than 4 heartbeats old.
On finding such, it will attempt to restart the job."""
import time
import json
import FetchPlayerAndGames
import FetchPlayerUpdatesAndNewPlayers
import FetchAchievements
import threading
import threadRegistrationQueue as TRQ
import BuildAllForAllArenasSequentially
import ConfigHelper
from  SQLconnector import connectToSource

 
__terminateInstruction__ = False
def startMonitorThreads():
    thread = threading.Thread(target=executeMonitor)
    thread.name = "HeartMonitor" 
    thread.start()
    return thread

def executeMonitor():
    time.sleep(5)
    conn = connectToSource()
    cursor = conn.cursor()
    SQL = """
            select age,"desc",ID,methodname,started,finished,lastheartbeat,resumeindex, methodParams, healthstatus,percenttocompletion, countofblocking
            from public."jobsView"
            where
                healthstatus = 'dead'
            order by lastheartbeat asc, started asc
 """
    activeThreads = []
    seconds = 29
    while not isTerminated():
        seconds = seconds + 1

        #print("TIME: %s, remainder: %s" % (seconds,seconds % 30 ))
        if seconds % 30 == 0: #every 30th second
            seconds = 0
            cursor.execute(SQL)
            conn.commit()
            #print ("---")
            for result in cursor.fetchall():
                if result[3] == "FetchPlayerAndGames.executeQueryGames":
                    MaxThreads = ConfigHelper.getConfigString("MaxWorkerThreads")
                    threadName = "%s:%s" % (result[2][0:3],result[1])
                    if checkThread(activeThreads,threadName) == 0 :
                    
                        params = json.loads(result[8])
                        FetchPlayerAndGames.QueryGamesLoad(params["scope"],offset=result[7],ID=result[2])
                        counter = 0 
                        while checkThread(activeThreads,threadName) < MaxThreads:
                            counter = counter + 1 
                            offset = 0
                            if result[7] != None:
                                offset = result[7]
                            print("Debug insertion")
                            t = threading.Thread(
                                target=FetchPlayerAndGames.QueryGamesLoop, 
                                args={result[2]}, 
                                kwargs={"counter":offset +  counter}) #
                            t.name = threadName
                            t.start()
                            activeThreads.append(t)
                            TRQ.q.put(t)

                    
                
                elif result[3] == "FetchPlayerUpdatesAndNewPlayers.updateExistingPlayers":
                    MaxThreads = ConfigHelper.getConfigString("MaxWorkerThreads")
                    threadName = "%s:%s" % (result[2][0:3],result[1])
                    if checkThread(activeThreads,threadName) == 0:
                        FetchPlayerUpdatesAndNewPlayers.updateExistingPlayersLoad(JobID=result[2])
                    while checkThread(activeThreads,threadName) < MaxThreads:
                        t = threading.Thread(
                            target=FetchPlayerUpdatesAndNewPlayers.updateExistingPlayersLoop, 
                            kwargs={"JobID":result[2]}
                        ) #this method gets offset from the job ID
                        t.name = threadName
                        t.start()
                        activeThreads.append(t)
                        TRQ.q.put(t)
                    

                    #execute known method.



                elif result[3] == "FetchAchievements.executeFetchAchievements":
                    MaxThreads = ConfigHelper.getConfigString("MaxWorkerThreads")
                    threadName = "%s:%s" % (result[2][0:3],result[1])
                    params = json.loads(result[8])
                    if checkThread(activeThreads,threadName) == 0:
                        FetchAchievements.FetchAchievementsLoad(params["scope"],jobID=result[2],offset=result[7])
                    while checkThread(activeThreads,threadName) < MaxThreads:

                        t = threading.Thread(
                            target=FetchAchievements.FetchAchievementsLoop, 
                            args=(params["scope"],), 
                            kwargs={"jobID":result[2],}) #
                        t.name = "%s:%s" % (result[2][0:3],result[1])
                        t.start()
                        activeThreads.append(t)
                        TRQ.q.put(t)




                elif result[3] == "FetchPlayerUpdatesAndNewPlayers.findNewPlayers":
                    MaxThreads = ConfigHelper.getConfigString("MaxWorkerThreads")
                    params = json.loads(result[8])
                    t = threading.Thread(
                        target=FetchPlayerUpdatesAndNewPlayers.findNewPlayers, 
                        #args=(params["siteName"],), 
                        kwargs={"jobID":result[2],"siteName":params["siteName"]}
                        ) #
                    t.name = "%s:%s" % (result[2][0:3],result[1])
                    if checkThread(activeThreads,t.name) == 0:
                        t.start()
                        activeThreads.append(t)
                        TRQ.q.put(t)



                elif result[3] == "buildAllForAllArenasSequentially.buildAllForAllArenasSequentially":
                    MaxThreads = ConfigHelper.getConfigString("MaxWorkerThreads")
                    t = threading.Thread (
                        target=BuildAllForAllArenasSequentially.buildAllForAllArenasSequentially,
                        kwargs={"jobID":result[2],"startIndex":result[7]}
                    )
                    
                    t.name = "%s:%s" % (result[2][0:3],result[1])
                    if checkThread(activeThreads,t.name) == 0:
                        t.start()
                        activeThreads.append(t)
                        TRQ.q.put(t)

                #print(result)
        time.sleep(1) #sleep for a second to allow termination checks

def checkThread(threads,threadTitle):
    counter = 0
    for t in threads:
        if t.name == threadTitle and t.isAlive():
            counter = counter + 1
        if not t.isAlive():
            threads.remove(t)
    return counter

def terminateMonitor():
    global __terminateInstruction__
    __terminateInstruction__ = True
    return

def isTerminated():
    global __terminateInstruction__
    return __terminateInstruction__


#FetchAchievements.executeFetchAchievements('recent',jobID='7e0b0aec-6a90-4672-ba75-1c676f69cb3c',offset=86)