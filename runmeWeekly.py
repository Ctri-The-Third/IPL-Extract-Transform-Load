import SQLHelper
import ConfigHelper as cfg
import string

cfg.setActive(0)
offset = 0 

params = {"arenaName":cfg.getConfigString("ArenaName"),"scope":"limited"}
targetIDs = SQLHelper.getInterestingPlayersRoster(False,cfg.getConfigString("StartDate"),cfg.getConfigString("ChurnDuration"),offset=offset,siteName = params["arenaName"])
SQLHelper.jobStart("Fetch games, [%s] active players " % (cfg.getConfigString("SiteNameShort")),0,"FetchPlayerAndGames.executeQueryGames",params,len(targetIDs),delay=-2) 


cfg.setActive(1)
params = {"arenaName":cfg.getConfigString("ArenaName"),"scope":"limited"}
targetIDs = SQLHelper.getInterestingPlayersRoster(False,cfg.getConfigString("StartDate"),cfg.getConfigString("ChurnDuration"),offset=offset,siteName = params["arenaName"])
SQLHelper.jobStart("Fetch games, [%s] active players " % (cfg.getConfigString("SiteNameShort")),0,"FetchPlayerAndGames.executeQueryGames",params,len(targetIDs),delay=-2) 


cfg.setActive(2)
params = {"arenaName":cfg.getConfigString("ArenaName"),"scope":"limited"}
targetIDs = SQLHelper.getInterestingPlayersRoster(False,cfg.getConfigString("StartDate"),cfg.getConfigString("ChurnDuration"),offset=offset,siteName = params["arenaName"])
SQLHelper.jobStart("Fetch games, [%s] active players " % (cfg.getConfigString("SiteNameShort")),0,"FetchPlayerAndGames.executeQueryGames",params,len(targetIDs),delay=-2) 


cfg.setActive(3)
params = {"arenaName":cfg.getConfigString("ArenaName"),"scope":"limited"}
targetIDs = SQLHelper.getInterestingPlayersRoster(False,cfg.getConfigString("StartDate"),cfg.getConfigString("ChurnDuration"),offset=offset,siteName = params["arenaName"])
SQLHelper.jobStart("Fetch games, [%s] active players " % (cfg.getConfigString("SiteNameShort")),0,"FetchPlayerAndGames.executeQueryGames",params,len(targetIDs),delay=-2) 

targetIDs = SQLHelper.getPlayersWhoMightNeedAchievementUpdates("recent")
params = {"scope":"recent"}
SQLHelper.jobStart("Fetch achievements, players from the last 7 days",0,"FetchAchievements.executeFetchAchievements",params,len(targetIDs),delay=20)

print ("Jobs queued! Would you like to continue and launch the main program?")
validInput = False
while validInput == False:
    inp = input("(y/n) ").lower()
    validInput = (inp == "y" or inp == "n")
    
if validInput == "y":
    import CmdMenus