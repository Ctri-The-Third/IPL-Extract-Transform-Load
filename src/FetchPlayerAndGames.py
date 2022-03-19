import math 


from datetime import datetime, timedelta
from FetchHelper import fetchPlayer_root
from FetchHelper import fetchPlayerRecents_root
from SQLHelper import addPlayer, updateGameFetchMetrics
from SQLHelper import addGame 
from SQLHelper import addParticipation
from SQLHelper import getInterestingPlayersRoster
from SQLHelper import jobStart, jobHeartbeat, jobEnd
import ConfigHelper as cfg

from queue import Queue
from threading import Thread

import sys
import logging

FULL_SCOPE = "full"
ONLY_ACTIVE_SCOPE = "activePlayers"
ONLY_ACTIVE_LOCAL_SCOPE = "localActivePlayers"

class LFFetchController(): 
    def __init__(self,update_scope,arena_name=None, interval = "Null", offset = None, ID = None, thread_count = 1 ) -> None:
        self.lo = logging.getLogger("FetchPlayerAndGames.LFFetchController")
        self.player_ids_to_query = Queue()
        self.scope = update_scope
        self.job_id = ID
        self.offset = offset
        self.interval = interval
        self.daemon = False 
        self.threads = [] 
        self._thread_count = thread_count
        
        self._updated_player_list = []
        
        self.load_player_ids_to_query()
        
        self._max_player_count = self.player_ids_to_query.qsize()
        pass

 #The query starts at the date in question and looks backwards. We use the "End Date" from the config.
#targetIDs = getInterestingPlayersRoster(False,cfg.getConfigString("EndDate'],cfg.getConfigString("ChurnDuration'])


#targetIDs = {
#    '7-8-0839' 
#}

    def load_player_ids_to_query(self):
        params = {}
        params["scope"] = self.scope
        params["arenaName"] = cfg.getConfigString("SiteNameReal")
        if self.scope == FULL_SCOPE: 
            targetIDs = getInterestingPlayersRoster(True,cfg.getConfigString("StartDate"),cfg.getConfigString("ChurnDuration"),offset=self.offset)
            if self.job_id == None: #new job
                self.job_id = jobStart("Fetch games, all players",0,"FetchPlayerAndGames.executeQueryGames",params,len(targetIDs),delay=-2)
        elif self.scope == ONLY_ACTIVE_SCOPE:
            targetIDs = getInterestingPlayersRoster(False,cfg.getConfigString("StartDate"),cfg.getConfigString("ChurnDuration"),offset=self.offset,siteName =  None)
            if self.job_id == None: #new job
                self.job_id = jobStart("Fetch games, All arenas active players " ,0,"FetchPlayerAndGames.executeQueryGames",params,len(targetIDs), delay=-2) 
        elif self.scope == ONLY_ACTIVE_LOCAL_SCOPE: 
            targetIDs = getInterestingPlayersRoster(False,cfg.getConfigString("StartDate"),cfg.getConfigString("ChurnDuration"),offset=self.offset,siteName = params["arenaName"])
            if self.job_id == None: #new job
                self.job_id = jobStart("Fetch games, [%s] active players " % (cfg.getConfigString("SiteNameShort")),0,"FetchPlayerAndGames.executeQueryGames",params,len(targetIDs), delay=-2) 
        else:
            self.lo.warning("Bad scope supplied to load_player_ids_to_query")

        for targetID in targetIDs:
            self.player_ids_to_query.put(targetID)
        
  
    def _loop_query_player_games (self):
        self.lo.info("Starting new thread")
        counter = self._max_player_count - self.player_ids_to_query.qsize() 
        job_id = self.job_id
        queue = self.player_ids_to_query
        jobHeartbeat(job_id,counter)
        eta = "Calculating"
        start_time = datetime.now()
        last_heartbeat = start_time
        while self.player_ids_to_query.empty() == False:
            target_id = queue.get()

            if  job_id != None:
                heartbeatDelta = ((datetime.now() - last_heartbeat).total_seconds()) 
                if heartbeatDelta > 30 or counter % 5 == 0:
                    jobHeartbeat(job_id,counter)
                    last_heartbeat = datetime.now()
            if counter >= 20:
                eta = self._get_eta(start_time,counter)
            else:
                eta = "Calculating"
            

            
            current_action = "Seeking games for %s, [%i / %i] : " % (target_id,counter,self._max_player_count)
            self.lo.info(current_action)
            self.status = current_action
            self.short_status = "games for %s" % (target_id)
            self.eta_str = eta 
            
            counter += 1 
            
            self.query_individual(target_id)
        self._announce_finish()
            
    def _announce_finish(self):
        self.lo.info("Thread finished")
    
        endTime = datetime.now()
        #f = open("Stats.txt","a+")
        #f.write("Queried {0} players' recent games, operation completed after {1}. \t\n".format(len(targetIDs),endTime - startTime ))
        #f.close()
    def _get_eta(self, start_time:datetime,players_processed) -> str:
        delta = ((datetime.now() - start_time).total_seconds() / players_processed) 
        delta = (self._max_player_count - players_processed) * delta #seconds remaining
        seconds = round(delta,0)
        minutes = 0
        hours = 0

        if (seconds > 60 ):
            minutes = math.floor(seconds / 60)
            seconds = seconds % 60 
        if (minutes > 60):
            hours = math.floor(minutes / 60 )
            minutes = minutes % 60
        
        eta_str = "%ih, %im, %is" % (hours,minutes,seconds)

        return eta_str
            



    def execute_query_games(self):
        for i in range(self._thread_count):
            thread = Thread(target=self._loop_query_player_games,daemon=self.daemon)
            self.threads.append(thread)
            thread.start()
    #QueryGamesLoop(jobID,offset)

    def query_individual(self,target_id) -> bool:
        
        region = target_id.split("-")[0]
        site =  target_id.split("-")[1]
        IDPart = target_id.split("-")[2]
        scope = self.scope        
        summaryJson = fetchPlayer_root('',region,site,IDPart)

        if "ERROR" in summaryJson:
            return False
        if summaryJson is not None and len(summaryJson) > 0:
            #print(DBGstring)
            datetime_list = []
            missions = 0
            level = 0
            for i in summaryJson["centre"]:
                datetime_list.append (str(i["joined"]))
                missions += int(i["missions"])
                level = max(level,int(i["skillLevelNum"]))
            joined = min(datetime_list)
            codeName = str(summaryJson["centre"][0]["codename"])
            playerNeedsUpdated = addPlayer(target_id,codeName,joined,missions)

            
            if playerNeedsUpdated == True or scope == FULL_SCOPE:
                self._updated_player_list.append(target_id)
                missionsJson = fetchPlayerRecents_root('',region,site,IDPart)
                if missionsJson != None and "mission" in missionsJson:
                    for mission in missionsJson["mission"]:
                    
                        missionUUID = addGame(mission[0],mission[1],mission[2])
                        "FetchPlayerAndGames: %s, %s " % (missionUUID, mission)
                        addParticipation(missionUUID,target_id,mission[3])
                updateGameFetchMetrics(target_id)
    
    def manualTargetForGames(self, targetID):
        self.query_individual(targetID,"individual")


if __name__ == "__main__":
    
    format_str = "%(levelname)s:%(name)s:%(thread)d:%(threadName)s::%(message)s"
    logging.basicConfig(handlers=[logging.StreamHandler(sys.stdout)],level=logging.DEBUG,format=format_str)
    arena = "Funstation Ltd, Edinburgh, Scotland"
    controller = LFFetchController(FULL_SCOPE,arena,thread_count=3)
    controller.execute_query_games()
