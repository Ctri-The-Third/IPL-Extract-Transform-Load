import SQLHelper
import ConfigHelper
import string

ConfigHelper.setActive(0)
SQLHelper.getInterestingPlayersRoster(False,cfg.getConfigString("StartDate"),cfg.getConfigString("ChurnDuration"),offset=offset,siteName = params["arenaName"])
SQLHelper.jobStart("Fetch games, [%s] active players " % (cfg.getConfigString("SiteNameShort")),0,"FetchPlayerAndGames.executeQueryGames",params,len(targetIDs),delay=-2) 


ConfigHelper.setActive(1)
SQLHelper.getInterestingPlayersRoster(False,cfg.getConfigString("StartDate"),cfg.getConfigString("ChurnDuration"),offset=offset,siteName = params["arenaName"])
SQLHelper.jobStart("Fetch games, [%s] active players " % (cfg.getConfigString("SiteNameShort")),0,"FetchPlayerAndGames.executeQueryGames",params,len(targetIDs),delay=-2) 


ConfigHelper.setActive(2)
SQLHelper.getInterestingPlayersRoster(False,cfg.getConfigString("StartDate"),cfg.getConfigString("ChurnDuration"),offset=offset,siteName = params["arenaName"])
SQLHelper.jobStart("Fetch games, [%s] active players " % (cfg.getConfigString("SiteNameShort")),0,"FetchPlayerAndGames.executeQueryGames",params,len(targetIDs),delay=-2) 


ConfigHelper.setActive(3)
SQLHelper.getInterestingPlayersRoster(False,cfg.getConfigString("StartDate"),cfg.getConfigString("ChurnDuration"),offset=offset,siteName = params["arenaName"])
SQLHelper.jobStart("Fetch games, [%s] active players " % (cfg.getConfigString("SiteNameShort")),0,"FetchPlayerAndGames.executeQueryGames",params,len(targetIDs),delay=-2) 

targetIDs = SQLHelper.getPlayersWhoMightNeedAchievementUpdates(scope)
jobStart("Fetch achievements, players from the last 7 days",0,"FetchAchievements.executeFetchAchievements",params,len(targetIDs))

print ("Jobs queued! Would you like to continue and launch the main program?")
validInput = False
while validInput == False:
    inp = input("(y/n) ").lower()
    validInput = (inp == "y" or inp == "n")
    
if validInput == "y":
    import CmdMenus