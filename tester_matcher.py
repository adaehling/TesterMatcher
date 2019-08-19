import sys
from database import database

def main():
    database.createDbConnection()
    allCountries = database.getAvailableCountries()
    allDevices = database.getAvailableDevices()

    countryPicker = {}
    count = 1
    for country in allCountries:
        # the query result is somehow turning each returned row into a tuple with the country as the first time, and an empty string as the second
        countryPicker[str(count)] = country[0]
        count += 1

    for key,value in countryPicker.items():
        print(key, ':', value)
    countryChoice = input("Please enter your choice of desired countries from the previous list. Enter 'All' to choose all countries. Separate multiple choices with a comma.\n")
    
    devicePicker = {}
    for device in allDevices:
        devicePicker[str(device[0])] = device[1].replace('\'','')

    for key,value in devicePicker.items():
        print(key, ':', value)
    deviceChoice = input("\nPlease enter your choice of devices. Enter 'All' to choose all devices. Separate multiple choices with a comma.\n")
        


if __name__ == '__main__':
    main()
