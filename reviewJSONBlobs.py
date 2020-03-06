import re
import json
#show the top 5
#show the top 10 stars 
#show the top 10 monthly games

targetBlobs = input("enter the ID of the blobs you want to investigat (e.g. 7-9) \n")
exe = re.compile(r'([0-9]+-[0-9]+)')
result = exe.match(targetBlobs) 
if not result:
    print("Regex didn't match %s. Abandoning" % exe)
    exit()
target = exe.findall(targetBlobs)[0]

#top5
outStr = (("--Results of Player Blob %s --"%targetBlobs)+"-"*40)[0:40]
print(outStr)

top5File = open("JSONBlobs/%s-playerBlob.json" % target)
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



#Stars!
outStr = (("--Star Quality for  %s --"%targetBlobs)+"-"*40)[0:40]
print(outStr)
   