import requests
import json
import importlib
import datetime

from FetchUsers import fetchPlayer_root
from FetchUsers import fetchPlayerRecents_root
from SQLconnector import addPlayer
from SQLconnector import addGame
from SQLconnector import addParticipation
targetIDs = {
    
'9-6-106', #C'tri
'7-9-0121', #Inferno
'7-9-0126', #Achilles
'7-9-0131', #Slamduck
'7-9-0195', #Pickle Rick
'7-9-0199', #Harley
'7-9-0219', #Explosion
'7-9-0238', #Oscar
'7-9-0358', #M3gan
'7-9-0435', #Cheese Sandwich
'7-9-0540', #OGHoe
'7-9-0562', #PlagueDoctor
'7-9-0563', #JammyDodger
'7-9-0588', #Phoenix
'7-9-0937', #Scottie Boy
'7-9-0950', #Tim
'7-9-0986', #Deadpool
'7-9-220040', #Rayth
'7-9-1115', #SuStar
'7-9-1205', #Rosco
'7-9-1298', #Ross
'7-9-1393', #Sir RodgerMoore
'7-9-1503', #Yannik
'7-9-1699', #Kyle R
'7-9-1700', #Terminator
'7-9-1979', #Ryry
'7-9-1981', #Minnie
'7-9-1996', #Paradigm
'7-9-2080', #Arran
'7-9-2081', #Glen
'7-9-2297', #Kayo Bupkis
'7-9-2331', #Reboot
'7-9-2418', #Aiden
'7-9-2637', #Logan
'7-9-2648', #Nathan B
'7-9-2659', #Smokey Bandit
'7-9-2783', #Grumpydad
'7-9-2828', #Psycho
'7-9-2893', #Maverick
'7-9-2999', #SuperDan
'7-9-3243', #Mr Spock
'7-9-3285', #Arran
'7-9-3363', #Mohamed
'7-9-3457', #Turtle
'7-9-3459', #Paton
'7-9-3763', #Dave
'7-9-3770', #Aiden
'7-9-3795', #Nbtglen
'7-9-4197', #Shooty McPewPew
'7-9-4500', #Gary
'7-9-4804', #Shogg
'7-9-4914', #Point Blank
'7-9-5322', #Eddie
'7-9-5323', #Char bar
'7-9-5428', #FaZe Celmestra
'7-9-5500', #Sean
'7-9-5501', #Lynda
'7-9-5521', #pIRATE
'7-9-5543', #Erratic
'7-9-5939', #Mindi
'7-9-6114', #Yoda
'7-9-7297', #Charlie
'7-9-7644', #Ninja
'7-9-7771', #Korg
'7-9-7925', #Ebony Falcon
'7-9-7955', #Lightning
'7-9-8167', #Billybob
'7-9-8263', #Zak Ras 32
'7-9-7297', #Charlie
'7-9-7644', #Ninja
'7-9-7771', #Korg
'7-9-7925', #Ebony Falcon
'7-9-7955', #Lightning
'7-9-8167', #Billybob
'7-9-8263', #Zak Ras 32
'7-9-8548', #Spencer
'7-9-8550', #Campbell
'7-9-8650', #Marc
'7-9-9024', #Murray
'7-9-9039', #Iain
'7-9-9298', #Troxx
'7-9-9299', #Ghost 57
'7-9-9310', #Dodey
'7-9-9311', #Jellybelly
'7-9-9337', #Mike Hunt
'7-9-9437', #Shadow
'7-9-9809', #��ayth
'7-9-9934', #BlazerFace43
'7-9-10283', #Achilles Jr
'7-9-10594', #Overdrive
'7-9-10594', #Overdrive
'7-9-11215', #Dikaiopolis
'7-9-11566', #HotShot
'7-9-11662', #Tiger
'7-9-11927', #ConIsABon
'7-9-12608', #D��mon L��rd
'7-9-12671', #Ki��g K��bra
'7-9-12699', #Godspeed
'7-9-13641', #ThatGuysFriend
'7-9-13915', #Jj
'7-9-13950', #Kyurin
'7-9-13958', #Robo_h34d
'7-9-14006', #Pinch
'7-8-1196', #Goku
'7-9-11663', #Soul
'7-9-9517', #Oreos
'7-9-9518', #Pedro
'7-9-13869', #Channa Banana

}
targetIDs = {
    '7-9-13869', #Channa Banana
}

for ID in targetIDs:
    region = ID.split("-")[0]
    site =  ID.split("-")[1]
    IDPart = ID.split("-")[2]
    print("DBG: %s-%s-%s" % (region,site,IDPart))
    summaryJson = fetchPlayer_root('',region,site,IDPart)
    if summaryJson is not None:
        datetime_list = []
        missions = 0
        level = 0
        for i in summaryJson["centre"]:
            datetime_list.append (str(i["joined"]))
            missions += int(i["missions"])
            level = max(level,int(i["skillLevelNum"]))
        joined = min(datetime_list)
        codeName = str(summaryJson["centre"][0]["codename"])
        addPlayer(ID,codeName,joined,missions,level)
    
        missionsJson = fetchPlayerRecents_root('',region,site,IDPart)
        for mission in missionsJson["mission"]:
            
            missionUUID = addGame(mission[0],mission[1],mission[2])
            "FetchPlayerAndGames: %s, %s " % (missionUUID, mission)
            addParticipation(missionUUID,ID,mission[3])
    else:
        print("Didn't find %s" % ID)

#iterate through the above and fetch stats for all.
#iterate through all players received and update / import player info
#iterate through all games played and create game records, and player associations.