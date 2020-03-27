import ConfigHelper
import SQLHelper


def queueWeekly():
    cfg = ConfigHelper.getConfig()
    #WEEKLY UPDATE
    #66
    params = {}
    params["scope"] = "activePlayers"
    params["arenaName"] = ConfigHelper.getConfigString("SiteNameReal")
    targetIDs = SQLHelper.getInterestingPlayersRoster(False,ConfigHelper.getConfigString("StartDate"),ConfigHelper.getConfigString("ChurnDuration"),siteName =  None)
    gamesID = SQLHelper.jobStart("Fetch games, All arenas active players " ,0,"FetchPlayerAndGames.executeQueryGames",params,len(targetIDs), delay=-2) 


    #67
    params = {}
    params["scope"] = "activePlayers"
    targetIDs = SQLHelper.getInterestingPlayersRoster(False,ConfigHelper.getConfigString("StartDate"),ConfigHelper.getConfigString("ChurnDuration"),siteName =  None)
    achievesID = SQLHelper.jobStart("Fetch achievements, players from the last 7 days",0,"FetchAchievements.executeFetchAchievements",params,len(targetIDs), delay=-2)
    SQLHelper.jobBlock(gamesID,achievesID)
    
    #6
    renderID = SQLHelper.jobStart("Render all blobs",0 ,"buildAllForAllArenasSequentially.buildAllForAllArenasSequentially", None, len(cfg["configs"]), delay=-2)
    SQLHelper.jobBlock(achievesID,renderID)

def queueMonthly():
    cfg = ConfigHelper.getConfig()

    #661
    targetIDs = SQLHelper.getPlayers(0)
    summaryID = SQLHelper.jobStart("Fetch summaries, all known players",0,"FetchPlayerUpdatesAndNewPlayers.updateExistingPlayers",None,len(targetIDs), delay=-2)


    #667
    newPlayersIDs= []    
    for site in cfg["configs"]:
        params = {}
        params["siteName"] = site["SiteNameReal"]
        newPlayersID = SQLHelper.jobStart("  new players at [%s]" % params["siteName"],0,"FetchPlayerUpdatesAndNewPlayers.findNewPlayers",params, delay=-2)
        newPlayersIDs.append(newPlayersID)

        
    #666
    params = {}
    params["scope"] = "full"
    params["arenaName"] = ConfigHelper.getConfigString("SiteNameReal")
    targetIDs = SQLHelper.getInterestingPlayersRoster(True,ConfigHelper.getConfigString("StartDate"),ConfigHelper.getConfigString("ChurnDuration"),offset=0)
    gamesID = SQLHelper.jobStart("Fetch games, all players",0,"FetchPlayerAndGames.executeQueryGames",params,len(targetIDs), delay=-2)


    for newPlayerID in newPlayersIDs:
        SQLHelper.jobBlock(gamesID,newPlayersID)
        SQLHelper.jobBlock(newPlayerID,summaryID)

    #677
    targetIDs = SQLHelper.getInterestingPlayersRoster(False,cfg.getConfigString("StartDate"),cfg.getConfigString("ChurnDuration"), offset=0)
    achievesID=SQLHelper.jobStart("Fetch achievements, active players",0,"FetchAchievements.executeFetchAchievements",params,len(targetIDs), delay=-2)
    SQLHelper.jobBlock(gamesID,achievesID)
    
    #6
    renderID = SQLHelper.jobStart("Render all blobs",0 ,"buildAllForAllArenasSequentially.buildAllForAllArenasSequentially", None, len(cfg["configs"]), delay=-2)
    SQLHelper.jobBlock(achievesID,renderID)
    #render
