import re
import json
#show the top 5
#show the top 10 stars 
#show the top 10 monthly games

targetBlobs = input("enter the ID of the blobs you want to investigat (e.g. 7-9-)\n Leave blank to do ALL")
if targetBlobs != "":
    exe = re.compile(r'.*([0-9]+-[0-9]+-).*')
    result = exe.match(targetBlobs) 
    if not result:
        print("Regex didn't match %s. Abandoning" % exe)
        exit()
    targets = exe.findall(targetBlobs)
else:
    #openCfg
    #Create array of targets
    cfgFile = open("AppConfig.json")
    cfgObj = json.load(cfgFile)
    print (json.dumps(cfgObj,indent=2))
    targets = []
    for config in cfgObj["configs"]:
        targets.append(config["ID Prefix"])

for target in targets:
    try:
        #top5
        outStr = (("\n--Results of Player Blob %s --"%target)+"-"*40)[0:40]
        print(outStr)

        top5File = open("JSONBlobs/%splayerBlob.json" % target)
        top5obj = json.load(top5File)
        #print (top5obj)
        definitions = ['GoldenPlayer','SilverPlayer','BronzePlayer','OtherPlayer1','OtherPlayer2']
        for definition in definitions:
            try:
                print ("%s\t%s games, \t%s stars, %s of %s" % (
            (top5obj[definition]['PlayerName']+" "*15)[0:15] ,
            top5obj[definition]['MonthlyGamesPlayed'] ,
            top5obj[definition]['StarQuality'] ,
            top5obj[definition]['SkillLevelName'] ,
            top5obj[definition]['HomeArenaTrunc'][0:15] ))
            
            except:
                print ("ERROR: Validation of %s failed" % definition)
    except:
        print ("ERROR: missing %s for big 5 in %s" %(definition,target))
    top5File.close()


    #Stars!
    outStr = (("\n--Star Quality for  %s --"%target)+"-"*40)[0:40]
    print(outStr)
    starFile = open("JSONBlobs/%sStarQuality.json" % target)
    starObj = json.load(starFile)

    outStr = (("--Starting %s and ending  %s --"%(starObj["ScoreLessDate"],starObj["ScoreGreaterOrEqualDate"])+"-"*40)[0:40])
    print (outStr)
    #print(json.dumps(starObj,indent=4))
    counter = 0
    while counter < 10:
        try:
            counter = counter + 1
            outStr = ((starObj["Player"][counter]["Name"]+" "*20)[0:20])
            outStr = outStr + ((starObj["Player"][counter]["StarQualityPerGame"]+" "*7)[0:7])
            outStr = outStr + (("%s"%(starObj["Player"][counter]["gamesPlayed"])+" "*7)[0:7])
            print (outStr)
        except:
            print("ERROR: Unable to processes SQ, player %s for %s ")
    input("Press enter to continue")