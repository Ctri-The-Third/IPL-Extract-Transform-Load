import pyodbc
import uuid


def connectToSource():

    conn = pyodbc.connect('Driver={SQL Server}; Server=CTRI-DESKTOP\SQLEXPRESS; Database=LaserScraper; Trusted_Connection=yes;')
    return conn