import SQLHelper
import SQLconnector
from psycopg2 import sql
import datetime

conn = SQLconnector.connectToSource()
cursor = conn.cursor()
SQL = """ select playerID, min(gametimestamp) from participation p join games g on g.gameuuid = p.gameuuid
group by 1 
"""

cursor.execute(SQL)
results = cursor.fetchall()
for result in results:
    print(result)
    newTime = result[1] 
    if result[1] < datetime.datetime(2019,5,17):
        newTime = datetime.datetime(2019,5,17)
    SQL = """update players set firstdetailupdate = %s where playerid = %s""" 
    cursor.execute(SQL,(newTime,result[0]))

conn.commit()
SQLconnector.closeConnection()