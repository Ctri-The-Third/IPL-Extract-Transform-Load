
# LF-Profiler
An application for retrieving data from http://iplaylaserforce.com


## Background

LaserForce is a brand of Laser Tag, developed in Brisbane and in venues around the world.

Part of the offering is a centralised aggregate scoreboard that can be accessed via a web-based interface for either global rankings, venue rankings, or individual progress.

## Purpose

This project is designed to extract and parse player information from the scoreboard.

Potential extensions from this core functionality extend to recording information and enriching it to provide additional data views and features such as:

 1. Mini embedable profile
 1. New scoreboard formattng
 2. Achievement point ranking
 3. Qualitative game ranking
 4. Monthly high scores

## Implementation

Python 3

## Installation instructions

1. download the source
2. install the requests library '''pip install requests'''
3. install the pyodbc library '''pip install pyodbc'''
5. The program currently expects a local SQLExpress - Run the <pre>DatabaseSetup.sql</pre> query
6. Set the connection string in SQLconnector.py


### Onboarding a new arena
1. Open the AppConfig.json file. 
2. to the "Configs" array, add a new dictionary with the following keys
 - SiteNameReal - the name of the site that is returned from IPL
 - SiteNameShort - a shortened alias for display
 - ID Prefix - A string in the form "#-#-" with the numbers representing the local membership numbering scheme. E.g. "7-9-" for members 7-9-###
3. Adjust the "big 5" query with the names of the "standard" games.