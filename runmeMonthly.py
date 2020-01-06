from SQLHelper import jobStart, getInterestingPlayersRoster
import ConfigHelper as cfg 

print("Scheduling Detailed sweep and achievements. MANUAL RUN SUMMARIES AND FIND-NEW")
params = {}
params["scope"] = "full"
targetIDs = getInterestingPlayersRoster(True,cfg.getConfigString("StartDate"),cfg.getConfigString("ChurnDuration"))
jobStart("Fetch games, all players",0,"FetchPlayerAndGames.executeQueryGames",params,len(targetIDs),delay=780)

targetIDs = getInterestingPlayersRoster(True,cfg.getConfigString("StartDate"),cfg.getConfigString("ChurnDuration"))
jobID=jobStart("Fetch achievements, inactive players",0,"FetchAchievements.executeFetchAchievements",params, len(targetIDs),delay=780+120)
