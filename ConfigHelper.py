import json

def getConfig(): 

    
    with open("AppConfig.json","r") as f:
        config  = json.load(f)

    return config


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

        return "Successfully set primary arena to [%s]" % (config["SiteNameReal"])

def setNewDates(startDate,endDate):
    return "not yet implemented"