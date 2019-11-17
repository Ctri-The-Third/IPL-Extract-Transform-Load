import SQLHelper
import FetchHelper
import re
import json
import ConfigHelper as cfg
print("7-4-104")
print ("Please enter 3 player IDs. If you get them wrong, start over.")
ID1 = input("ID 1: ")
if not (re.match('[0-9]*-[0-9]*-[0-9]*',ID1)):
    print("ID 1 didn't regex match")
    exit() 

matches = re.search('([0-9]*)-([0-9]*)-([0-9]*)',ID1)
playerJSON = FetchHelper.fetchPlayer_ID(matches.groups()[0],matches.groups()[1],matches.groups()[2])

if "centre" not  in playerJSON:
    print("Did not find player data, cannot onboard.")
    exit()

counter = 1
if len(playerJSON["centre"]) > 1:
    for centre in playerJSON["centre"]:
        print("[%s] %s" % (counter,centre["name"]))
        counter = counter + 1
    pickedArena = int(input ("Pick which of these is the main arena: \n"))
else:
    pickedArena = 1
pickedArena = pickedArena - 1
print ("\nArena Name: \t\t%s" % (playerJSON["centre"][pickedArena]["name"],))
print ("Arena Prefix: \t\t%s-%s-###" % (matches.groups()[0],matches.groups()[1]))
print(" Leave blank to use Arena Name")
shortName = input ("Arena short name:\t" )
if shortName == "":
    shortName = playerJSON["centre"][pickedArena]["name"]
    print("Arena short name:\t%s" % (shortName,))

print("\n\n\n")
print(json.dumps(playerJSON,indent=2))


newEntry = {"ID Prefix":"%s-%s-" % (matches.groups()[0],matches.groups()[1]),
"SiteNameReal":"%s" % (playerJSON["centre"][pickedArena]["name"],),
"SiteNameShort" : "%s" % (shortName,)}
cfg.addNewSite(newEntry)

conf = cfg.getConfig()
newID = len(conf["configs"])
cfg.setActive (newID)

print("Run main application, 667, then 661, then 677")