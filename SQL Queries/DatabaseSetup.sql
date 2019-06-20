USE [master]
GO

/****** Object:  Database [LaserScraper]    Script Date: 6/20/2019 10:00:01 AM ******/
CREATE DATABASE [LaserScraper]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'LaserScraper', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL14.SQLEXPRESS\MSSQL\DATA\LaserScraper.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
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

/****** Object:  Table [dbo].[Games]    Script Date: 6/20/2019 10:01:23 AM ******/
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

/****** Object:  Table [dbo].[Participation]    Script Date: 6/20/2019 10:01:28 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Participation](
	[PlayerID] [varchar](15) NOT NULL,
	[GameUUID] [varchar](50) NOT NULL,
	[Score] [int] NOT NULL,
 CONSTRAINT [PK_Participation] PRIMARY KEY CLUSTERED 
(
	[PlayerID] ASC,
	[GameUUID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO


USE [LaserScraper]
GO

/****** Object:  Table [dbo].[Players]    Script Date: 6/20/2019 10:01:32 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Players](
	[PlayerID] [varchar](15) NOT NULL,
	[GamerTag] [varchar](20) NOT NULL,
	[Joined] [date] NULL,
	[Missions] [int] NULL,
	[Level] [int] NULL
) ON [PRIMARY]
GO

