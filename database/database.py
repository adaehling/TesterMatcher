from pathlib import Path
import sqlite3
from sqlite3 import Error

bugsTableCreate = """CREATE TABLE bugs 
    (bugId int primary key,
    deviceId int,
    testerId int,
    foreign key (deviceId) references devices(deviceId))"""

devicesTableCreate = """CREATE TABLE devices 
    (deviceId int primary key,
    description text)"""

testerDeviceTableCreate = """CREATE TABLE tester_device 
    (testerId int,
    deviceId int,
    foreign key (testerId) references testers(testerId),
    foreign key (deviceId) references devices(deviceId))"""

testersTableCreate = """CREATE TABLE testers 
    (testerId int primary key,
    firstName text,
    lastName text,
    country text,
    lastLogin text)"""

bugsTableInsert = """insert into bugs (bugId, deviceId, testerId) values (?, ?, ?)"""
devicesTableInsert = """insert into devices (deviceId, description) values (?, ?)"""
testerDeviceTableInsert = """insert into tester_device (testerId, deviceId) values (?, ?)"""
testersTableInsert = """insert into testers (testerId, firstName, lastName, country, lastLogin) values (?, ?, ?, ?, ?)"""

getAllCountriesQuery = """select distinct country from testers"""

getAllDevicesQuery = """select * from devices"""

bugsDataFileLocation = Path('./testdata/bugs.csv').resolve()
devicesDataFileLocation = Path('./testdata/devices.csv').resolve()
testerDeviceDataFileLocation = Path('./testdata/tester_device.csv').resolve()
testersDataFileLocation = Path('./testdata/testers.csv').resolve()

dbConnection = None

"""
    Creates a connection to a SQLite database that resides in memory
"""
def createDbConnection():
    try:
        global dbConnection
        dbConnection = sqlite3.connect(':memory:')
        initializeDatabaseSchema()
        insertTestData()
    except Error as e:
        print(e)


def initializeDatabaseSchema():
    try:
        cursor = dbConnection.cursor()
        cursor.execute(bugsTableCreate)
        cursor.execute(devicesTableCreate)
        cursor.execute(testerDeviceTableCreate)
        cursor.execute(testersTableCreate)
    except Exception as e:
        print(e)

def insertTestData():
    cursor = dbConnection.cursor()

    # duplicated code should be its own routine
    with open(bugsDataFileLocation, 'r') as f:
        content = f.readlines()
    for line in content[1:]:
        values = line.replace('"','').split(',')
        cursor.execute(bugsTableInsert, (values[0], values[1], values[2]))

    with open(devicesDataFileLocation, 'r') as f:
        content = f.readlines()
    for line in content[1:]:
        values = line.replace('"','').replace('\n','').split(',')
        cursor.execute(devicesTableInsert, (values[0], values[1]))

    with open(testerDeviceDataFileLocation, 'r') as f:
        content = f.readlines()
    for line in content[1:]:
        values = line.replace('"','').split(',')
        cursor.execute(testerDeviceTableInsert, (values[0], values[1]))

    with open(testersDataFileLocation, 'r') as f:
        content = f.readlines()
    for line in content[1:]:
        values = line.replace('"','').split(',')
        cursor.execute(testersTableInsert, (values[0], values[1], values[2], values[3], values[4]))

# returns the list of countries to choose from
def getAvailableCountries():
    cursor = dbConnection.cursor()
    cursor.execute(getAllCountriesQuery)
    return cursor.fetchall()

# returns the list of devices to choose from
def getAvailableDevices():
    cursor = dbConnection.cursor()
    cursor.execute(getAllDevicesQuery)
    return cursor.fetchall()

# executes the query to return the tester results based on user input
# on selected country(ies) and device(s)
def matchTesters():
    print("db")