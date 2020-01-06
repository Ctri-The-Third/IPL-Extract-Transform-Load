import json
import re
from DBG import DBG

configPath = "AppConfig.json"
config = {}
def getConfig(): 
    global configPath
    global config
    with open(configPath,"r") as f:
        config  = json.load(f)
    return config

def getConfigString(string):
    global config 

    if config == {}:
        getConfig()
    if string in config:
        return config[string]
    DBG("CONFIG key ['%s'] not found" % string,2 )


def setActive(index):
    global configPath
    with open(configPath,"r") as f:
        config  = json.load(f)

        foundConfigs = "configs" in config
        if not foundConfigs:
            return "Failed, didn't find config object in config"
        foundConfigIndex = len(config["configs"]) >= (index + 1)
        if not foundConfigIndex:
            return "Failed, didn't find config %i" % (index)
        
        config["SiteNameReal"] = config["configs"][index]["SiteNameReal"]
        config["SiteNameShort"] = config["configs"][index]["SiteNameShort"]
        config["ID Prefix"] = config["configs"][index]["ID Prefix"]

        f = open(configPath, "w+")
        f.write(json.dumps(config,indent=2))
        f.close()
        getConfig()
        return "Successfully set primary arena to [%s]" % (config["SiteNameReal"])

def setNewDates(startDate,endDate):
    global configPath
    with open(configPath,"r") as f:
        config  = json.load(f)

        x = re.search("([0-9]){4}-([0-9]){2}-([0-9]){2}",startDate)
        if not (x):
            return "Invalid start date"
        x = re.search("([0-9]){4}-([0-9]){2}-([0-9]){2}",endDate)
        if not (x):
            return "Invalid end date"
        
        config["StartDate"] = startDate
        config["EndDate"] = endDate

        f = open(configPath, "w+")
        f.write(json.dumps(config,indent=2))
        f.close()

        return "Successfully set start and end dates to [%s] and [%s]" % (config["StartDate"], config["EndDate"])

def addNewSite(obj):

    with open(configPath,"r") as f:
        config  = json.load(f)

        config["configs"].append(obj)

        f = open(configPath, "w+")
        f.write(json.dumps(config,indent=2))
        f.close()

        return "Successfully set start and end dates to [%s] and [%s]" % (config["StartDate"], config["EndDate"])


def getSiteWithoutActivatingByID(id):
    config = getConfig()

    return config["configs"][id] 

def findSiteIDFromName(name):
    obj = getConfig()
    counter = 0
    for centre in obj["configs"]:
        if centre["SiteNameReal"] == name:
            return counter
        counter = counter + 1
    
    return -1