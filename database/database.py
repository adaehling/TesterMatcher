import sqlite3
from sqlite3 import Error

"""
    Creates a connection to a SQLite database that resides in memory
"""
def createDbConnection():
    try:
        global:dbConnection = sqlite3.connect(':memory:')
        return dbConnection
    except Error as e:
        print(e)

def readDataFile(filePath):
    