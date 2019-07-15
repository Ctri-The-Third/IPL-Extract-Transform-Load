from FetchPlayerAndGames import executeQueryGames
from FetchAchievements import executeFetchAchievements

from BuildMonthlyScoresToJSON import executeMonthlyScoresBuild
from BuildMonthlyStarQualityToJSON import executeBuildMonthlyStars
from BuildAchievementScoresToJSON import executeAchievementBuild
from BuildPlayerBlob import executeBuildPlayerBlobs
from BuildHeadToHeadsToJSON import buildHeadToHeads
from FetchPlayerUpdatesAndNewPlayers import updateExistingPlayers
from FetchPlayerUpdatesAndNewPlayers import findNewPlayers
from FetchPlayerAndGames import executeQueryGames
updateExistingPlayers()
findNewPlayers()

executeQueryGames()
executeFetchAchievements()
executeMonthlyScoresBuild()
executeBuildMonthlyStars()
executeAchievementBuild()
executeBuildPlayerBlobs()
buildHeadToHeads()
