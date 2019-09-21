#import pyodbc
import psycopg2

def connectToSource():
    conn = psycopg2.connect(host='localhost',user='ctri', password='Prayer1')
    #conn = pyodbc.connect('Driver={SQL Server}; Server=CTRI-DESKTOP\SQLEXPRESS; Database=LaserScraper; Trusted_Connection=yes;')
    return conn

def execute():
    result = {}
    return result 

connectToSource()