USE [master]
GO

/****** Object:  Database [LaserScraper]    Script Date: 27-Aug-19 12:06:17 ******/
CREATE DATABASE [LaserScraper]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'LaserScraper', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL14.SQLEXPRESS\MSSQL\DATA\LaserScraper.mdf' , SIZE = 73728KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'LaserScraper_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL14.SQLEXPRESS\MSSQL\DATA\LaserScraper_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
GO

IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [LaserScraper].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO

ALTER DATABASE [LaserScraper] SET ANSI_NULL_DEFAULT OFF 
GO

ALTER DATABASE [LaserScraper] SET ANSI_NULLS OFF 
GO

ALTER DATABASE [LaserScraper] SET ANSI_PADDING OFF 
GO

ALTER DATABASE [LaserScraper] SET ANSI_WARNINGS OFF 
GO

ALTER DATABASE [LaserScraper] SET ARITHABORT OFF 
GO

ALTER DATABASE [LaserScraper] SET AUTO_CLOSE OFF 
GO

ALTER DATABASE [LaserScraper] SET AUTO_SHRINK OFF 
GO

ALTER DATABASE [LaserScraper] SET AUTO_UPDATE_STATISTICS ON 
GO

ALTER DATABASE [LaserScraper] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO

ALTER DATABASE [LaserScraper] SET CURSOR_DEFAULT  GLOBAL 
GO

ALTER DATABASE [LaserScraper] SET CONCAT_NULL_YIELDS_NULL OFF 
GO

ALTER DATABASE [LaserScraper] SET NUMERIC_ROUNDABORT OFF 
GO

ALTER DATABASE [LaserScraper] SET QUOTED_IDENTIFIER OFF 
GO

ALTER DATABASE [LaserScraper] SET RECURSIVE_TRIGGERS OFF 
GO

ALTER DATABASE [LaserScraper] SET  DISABLE_BROKER 
GO

ALTER DATABASE [LaserScraper] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO

ALTER DATABASE [LaserScraper] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO

ALTER DATABASE [LaserScraper] SET TRUSTWORTHY OFF 
GO

ALTER DATABASE [LaserScraper] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO

ALTER DATABASE [LaserScraper] SET PARAMETERIZATION SIMPLE 
GO

ALTER DATABASE [LaserScraper] SET READ_COMMITTED_SNAPSHOT OFF 
GO

ALTER DATABASE [LaserScraper] SET HONOR_BROKER_PRIORITY OFF 
GO

ALTER DATABASE [LaserScraper] SET RECOVERY SIMPLE 
GO

ALTER DATABASE [LaserScraper] SET  MULTI_USER 
GO

ALTER DATABASE [LaserScraper] SET PAGE_VERIFY CHECKSUM  
GO

ALTER DATABASE [LaserScraper] SET DB_CHAINING OFF 
GO

ALTER DATABASE [LaserScraper] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO

ALTER DATABASE [LaserScraper] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO

ALTER DATABASE [LaserScraper] SET DELAYED_DURABILITY = DISABLED 
GO

ALTER DATABASE [LaserScraper] SET QUERY_STORE = OFF
GO

ALTER DATABASE [LaserScraper] SET  READ_WRITE 
GO


USE [LaserScraper]
GO

/****** Object:  Table [dbo].[AllAchievements]    Script Date: 27-Aug-19 12:19:17 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[AllAchievements](
	[AchName] [varchar](50) NOT NULL,
	[Description] [text] NOT NULL,
	[image] [varchar](64) NULL,
	[ArenaName] [varchar](50) NOT NULL,
	[AchID] [varchar](50) NOT NULL,
 CONSTRAINT [PK_AllAchievements] PRIMARY KEY CLUSTERED 
(
	[AchID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO



USE [LaserScraper]
GO

/****** Object:  Table [dbo].[Games]    Script Date: 27-Aug-19 12:19:28 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Games](
	[GameTimestamp] [datetime] NOT NULL,
	[GameName] [varchar](50) NOT NULL,
	[ArenaName] [varchar](50) NOT NULL,
	[GameUUID] [nvarchar](50) NOT NULL,
 CONSTRAINT [PK_Games] PRIMARY KEY CLUSTERED 
(
	[GameUUID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

USE [LaserScraper]
GO

/****** Object:  Table [dbo].[Participation]    Script Date: 27-Aug-19 12:19:38 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Participation](
	[PlayerID] [varchar](15) NOT NULL,
	[GameUUID] [varchar](50) NOT NULL,
	[Score] [int] NOT NULL,
	[insertedTimestamp] [datetime] NULL,
 CONSTRAINT [PK_Participation] PRIMARY KEY CLUSTERED 
(
	[PlayerID] ASC,
	[GameUUID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

USE [LaserScraper]
GO

/****** Object:  Table [dbo].[PlayerAchievement]    Script Date: 27-Aug-19 12:19:45 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[PlayerAchievement](
	[AchID] [varchar](50) NOT NULL,
	
	[PlayerID] [varchar](50) NOT NULL,
	[newAchievement] [int] NULL,
	[achievedDate] [date] NULL,
	[progressA] [int] NULL,
	[progressB] [int] NULL,
 CONSTRAINT [PK_PlayerAchievement] PRIMARY KEY CLUSTERED 
(
	[AchID] ASC.
	[PlayerID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

USE [LaserScraper]
GO

/****** Object:  Table [dbo].[Players]    Script Date: 27-Aug-19 12:19:50 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Players](
	[PlayerID] [varchar](15) NOT NULL,
	[GamerTag] [varchar](20) NOT NULL,
	[Joined] [date] NULL,
	[Missions] [int] NULL,
	[Level] [int] NULL,
	[AchievementScore] [int] NULL
) ON [PRIMARY]
GO

USE [LaserScraper]
GO

/****** Object:  View [dbo].[InterestingPlayers]    Script Date: 27-Aug-19 12:20:00 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [dbo].[InterestingPlayers]
AS
SELECT        TOP (100) PERCENT dbo.Players.Missions, dbo.Players.[Level], dbo.Players.PlayerID, dbo.MostRecentGame.mostRecent, CASE WHEN dbo.MostRecentGame.mostRecent < DATEADD(day, - 60, GETDATE()) 
                         THEN 'Churned' ELSE 'Active' END AS SeenIn60Days
FROM            dbo.Players LEFT OUTER JOIN
                         dbo.MostRecentGame ON dbo.Players.PlayerID = dbo.MostRecentGame.PlayerID
WHERE        (dbo.Players.Missions > 15) OR
                         (dbo.Players.[Level] >= 4)
GO

EXEC sys.sp_addextendedproperty @name=N'MS_DiagramPane1', @value=N'[0E232FF0-B466-11cf-A24F-00AA00A3EFFF, 1.00]
Begin DesignProperties = 
   Begin PaneConfigurations = 
      Begin PaneConfiguration = 0
         NumPanes = 4
         Configuration = "(H (1[40] 4[20] 2[20] 3) )"
      End
      Begin PaneConfiguration = 1
         NumPanes = 3
         Configuration = "(H (1 [50] 4 [25] 3))"
      End
      Begin PaneConfiguration = 2
         NumPanes = 3
         Configuration = "(H (1 [50] 2 [25] 3))"
      End
      Begin PaneConfiguration = 3
         NumPanes = 3
         Configuration = "(H (4 [30] 2 [40] 3))"
      End
      Begin PaneConfiguration = 4
         NumPanes = 2
         Configuration = "(H (1 [56] 3))"
      End
      Begin PaneConfiguration = 5
         NumPanes = 2
         Configuration = "(H (2 [66] 3))"
      End
      Begin PaneConfiguration = 6
         NumPanes = 2
         Configuration = "(H (4 [50] 3))"
      End
      Begin PaneConfiguration = 7
         NumPanes = 1
         Configuration = "(V (3))"
      End
      Begin PaneConfiguration = 8
         NumPanes = 3
         Configuration = "(H (1[56] 4[18] 2) )"
      End
      Begin PaneConfiguration = 9
         NumPanes = 2
         Configuration = "(H (1 [75] 4))"
      End
      Begin PaneConfiguration = 10
         NumPanes = 2
         Configuration = "(H (1[66] 2) )"
      End
      Begin PaneConfiguration = 11
         NumPanes = 2
         Configuration = "(H (4 [60] 2))"
      End
      Begin PaneConfiguration = 12
         NumPanes = 1
         Configuration = "(H (1) )"
      End
      Begin PaneConfiguration = 13
         NumPanes = 1
         Configuration = "(V (4))"
      End
      Begin PaneConfiguration = 14
         NumPanes = 1
         Configuration = "(V (2))"
      End
      ActivePaneConfig = 0
   End
   Begin DiagramPane = 
      Begin Origin = 
         Top = 0
         Left = 0
      End
      Begin Tables = 
         Begin Table = "Players"
            Begin Extent = 
               Top = 6
               Left = 38
               Bottom = 136
               Right = 226
            End
            DisplayFlags = 280
            TopColumn = 0
         End
         Begin Table = "MostRecentGame"
            Begin Extent = 
               Top = 6
               Left = 264
               Bottom = 102
               Right = 434
            End
            DisplayFlags = 280
            TopColumn = 0
         End
      End
   End
   Begin SQLPane = 
   End
   Begin DataPane = 
      Begin ParameterDefaults = ""
      End
   End
   Begin CriteriaPane = 
      Begin ColumnWidths = 11
         Column = 1440
         Alias = 900
         Table = 1170
         Output = 720
         Append = 1400
         NewValue = 1170
         SortType = 1350
         SortOrder = 1410
         GroupBy = 1350
         Filter = 1350
         Or = 1350
         Or = 1350
         Or = 1350
      End
   End
End
' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'VIEW',@level1name=N'InterestingPlayers'
GO

EXEC sys.sp_addextendedproperty @name=N'MS_DiagramPaneCount', @value=1 , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'VIEW',@level1name=N'InterestingPlayers'
GO

USE [LaserScraper]
GO

/****** Object:  View [dbo].[MostRecentGame]    Script Date: 27-Aug-19 12:20:09 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


CREATE VIEW [dbo].[MostRecentGame]
AS
SELECT        MAX(g.GameTimestamp) AS mostRecent, p.PlayerID
FROM            dbo.Participation AS p INNER JOIN
                         dbo.Games AS g ON p.GameUUID = g.GameUUID
GROUP BY p.PlayerID
GO



