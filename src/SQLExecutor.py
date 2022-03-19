from SQLconnector import connectToSource
import json
conn = connectToSource()
cursor = conn.cursor()

sqlfile = open("/home/ctri/github/LF-Profiler/SQL Queries/ArenaDemographics-allYear.sql")
SQL = sqlfile.read()#.replace('', '')

conn = connectToSource()
cursor = conn.cursor()

cursor.execute(SQL)
results = cursor.fetchall()
SQLdesc = cursor.description
descCount = 0
for desc in SQLdesc:
    print("%s %s" % (descCount,desc[0]))
    descCount = descCount + 1

currentMonth = ""
months = []
for result in results:
    
    print (result)