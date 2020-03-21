#import pyodbc
import psycopg2
import ConfigHelper
counter = 0
conn = None
def connectToSource():
    global conn
    global counter
    
    cfg = ConfigHelper.getConfig()
    
    if counter <= 0:
        conn = psycopg2.connect(host=cfg["DBConnectionString"]["host"],port=cfg["DBConnectionString"]["port"] ,user=cfg["DBConnectionString"]["username"], password=cfg["DBConnectionString"]["password"], database = cfg["DBConnectionString"]["database"])
        conn.set_session(autocommit = True)
    else:
        try:
            cursor = conn.cursor()
        except:
            print("It's closed but the Counter is %s" % (counter,))
            counter = 0 
            return connectToSource()
            
    #conn = psycopg2.connect(host='localhost',port=5432 ,user='LaserScraper', password='LaserScraper', database = 'LaserScraper')
    #conn = pyodbc.connect('Driver={SQL Server}; Server=CTRI-DESKTOP\SQLEXPRESS; Database=LaserScraper; Trusted_Connection=yes;')
    counter = counter + 1
    return conn

def closeConnection():
    global conn
    global counter
    counter = counter - 1
    if counter <= 0:
        conn.close()

def execute():
    result = {}
    return result 

    #SQL = databaseSetup.read()