DECLARE @SourceID as varchar(10);
DECLARE @TargetID as varchar(10);
SET @SourceID = '7-9-0126'
SET @TargetID = '7-9-126'
--358, 219

update PlayerAchievement set PlayerID = @TargetID where PlayerID = @SourceID;
update Participation set PlayerID = @TargetID where PlayerID = @SourceID;
delete from Players where PlayerID = @SourceID;
delete from Participation where PlayerID = @SourceID;
delete from PlayerAchievement where PlayerID = @SourceID;
select * from players where playerID like '7-9-0%'

