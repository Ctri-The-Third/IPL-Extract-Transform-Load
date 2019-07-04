import json

def getConfig(): 

    
    with open("AppConfig.json","r") as f:
        config  = json.load(f)

    return config
