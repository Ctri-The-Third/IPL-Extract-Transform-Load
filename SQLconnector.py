#import pyodbc
import psycopg2

def connectToSource():
    conn = psycopg2.connect(host='localhost',port=5432 ,user='LaserScraper', password='LaserScraper', database = 'laserscraper')
    #conn = pyodbc.connect('Driver={SQL Server}; Server=CTRI-DESKTOP\SQLEXPRESS; Database=LaserScraper; Trusted_Connection=yes;')
    return conn

def execute():
    result = {}
    return result 

def setupPostgres():
    databaseSetup = open("SQL Queries/DatabaseSetup - postgresql.sql")
    SQL = databaseSetup.read()

    conn = connectToSource()
    print (conn)
    cursor = conn.cursor()

    result = cursor.execute(SQL)
    conn.commit()
    conn.close()
#setupPostgres()
conn = connectToSource()
cursor = conn.cursor()
cursor.execute ("select * from players")
print ("Credentials correct, database exist, tables exist")
print(cursor.fetchone())

