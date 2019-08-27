import json
import re
from DBG import DBG

config = {}
def getConfig(): 

    global config
    with open("AppConfig.json","r") as f:
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
    with open("AppConfig.json","r") as f:
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

        f = open("AppConfig.json", "w+")
        f.write(json.dumps(config,indent=2))
        f.close()
        getConfig()
        return "Successfully set primary arena to [%s]" % (config["SiteNameReal"])

def setNewDates(startDate,endDate):

    with open("AppConfig.json","r") as f:
        config  = json.load(f)

        x = re.search("([0-9]){4}-([0-9]){2}-([0-9]){2}",startDate)
        if not (x):
            return "Invalid start date"
        x = re.search("([0-9]){4}-([0-9]){2}-([0-9]){2}",endDate)
        if not (x):
            return "Invalid end date"
        
        config["StartDate"] = startDate
        config["EndDate"] = endDate

        f = open("AppConfig.json", "w+")
        f.write(json.dumps(config,indent=2))
        f.close()

        return "Successfully set start and end dates to [%s] and [%s]" % (config["StartDate"], config["EndDate"])

