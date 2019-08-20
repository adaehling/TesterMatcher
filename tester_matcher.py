import sys
from tkinter import *
from database import database

class Window(Frame):
    countryListbox = None
    deviceListbox = None
    resultsListbox = None

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        database.createDbConnection()
        self.initializeWindow()

    def initializeWindow(self):
        self.master.title("Tester Matcher")
        self.pack(fill=BOTH, expand=1)

        # create the button to initiate matching testers based on user input
        matchButton = Button(self, text="Match Testers", command=self.matchTesters)
        matchButton.place(x=470, y=400)
        
        # create the ListBox objects to display the country and device information
        Label(self, text="Select One or More Countries").place(x=20, y=0)
        self.countryListbox = Listbox(self, selectmode='multiple', height=20, width=25, exportselection=0)
        self.countryListbox.place(x=20, y=20)

        Label(self, text="Select One or More Devices").place(x=200, y=0)
        self.deviceListbox = Listbox(self, selectmode='multiple', height=20, width=30, exportselection=0)
        self.deviceListbox.place(x=200, y=20)

        Label(self, text="Tester Match Results:").place(x=450, y=0)
        self.resultsListbox = Listbox(self, height=20, width=30, exportselection=0)
        self.resultsListbox.place(x=450, y=20)
        scrollbar = Scrollbar(self, orient="vertical")
        scrollbar.config(command=self.resultsListbox.yview)
        scrollbar.place(x=632, y=22)
        scrollbar.pack(side="right", fill="y")
        self.resultsListbox.config(yscrollcommand=scrollbar.set)

        countries = self.getListOfCountries()
        count = 0
        for country in countries:
            # the query is returning each individual result as a tuple with the value of the country and an empty value
            self.countryListbox.insert(count, country[0])
            count += 1
            
        devices = self.getListOfDevices()
        for device in devices:
            self.deviceListbox.insert(device[0] - 1, device[1])

    def matchTesters(self):
        # clear the results listbox
        self.resultsListbox.delete('0', 'end')

        # returns index of selected choices
        selectedCountryIndices = self.countryListbox.curselection()
        selectedDeviceIndices = self.deviceListbox.curselection()

        countries = []
        for index in selectedCountryIndices:
            countries.append(self.countryListbox.get(index))

        devices = []
        for index in selectedDeviceIndices:
            devices.append(self.deviceListbox.get(index))
        
        result,firstNameKey = database.matchTesters(countries, devices)
        
        # sort dict by values
        sortedTupleList = sorted(result.items(), key=lambda x: x[1], reverse=True)

        index = 0
        for matchedTester in sortedTupleList:
            self.resultsListbox.insert(index, firstNameKey[matchedTester[0]] + '  :  ' + str(matchedTester[1]))
            index += 1


    def getListOfCountries(self):
        return database.getAvailableCountries()

    def getListOfDevices(self):
        return database.getAvailableDevices()


def main():
    root = Tk()
    root.geometry("800x600")
    app = Window(root)
    root.mainloop()

if __name__ == '__main__':
    main()
