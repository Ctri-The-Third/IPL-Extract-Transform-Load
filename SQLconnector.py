#import pyodbc
import psycopg2

def connectToSource():
    conn = psycopg2.connect(host='192.168.0.133',port=5432 ,user='LaserScraper', password='LaserScraper', database = 'LaserScraper')
    #conn = psycopg2.connect(host='localhost',port=5432 ,user='LaserScraper', password='LaserScraper', database = 'LaserScraper')
    #conn = pyodbc.connect('Driver={SQL Server}; Server=CTRI-DESKTOP\SQLEXPRESS; Database=LaserScraper; Trusted_Connection=yes;')
    return conn

def execute():
    result = {}
    return result 

    #SQL = databaseSetup.read()