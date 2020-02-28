import BuildMonthlyScoresToJSON
import BuildMonthlyStarQualityToJSON
import BuildAchievementScoresToJSON
import BuildPlayerBlob
import BuildHeadToHeadsToJSON
import BuildAnnualArenaMetrics
import BuildAnnualTop3s
import ConfigHelper as cfgH
def buildAllForAllArenasSequentially():
    cfg = cfgH.getConfig()
    counter = 0
    for config in cfg["configs"]:
        cfgH.setActive(counter)
        BuildMonthlyScoresToJSON.executeMonthlyScoresBuild()
        BuildMonthlyStarQualityToJSON.executeBuildMonthlyStars()
        BuildAchievementScoresToJSON.executeAchievementBuild()
        BuildPlayerBlob.executeBuildPlayerBlobs()
        #BuildHeadToHeadsToJSON.buildHeadToHeads()
        BuildAnnualArenaMetrics.executeBuild()
        BuildAnnualTop3s.execute()
        counter = counter + 1

buildAllForAllArenasSequentially()