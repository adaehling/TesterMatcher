import sys
from tkinter import *
from database import database

class Window(Frame):

    countrySelectionList = []
    deviceSelectionList = []
    countryListbox = None
    deviceListbox = None
    resultsListbox = None

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.initializeWindow()

    def initializeWindow(self):
        self.master.title("Tester Matcher")
        self.pack(fill=BOTH, expand=1)

        # create the button to initiate matching testers based on user input
        matchButton = Button(self, text="Match Testers", command=self.matchTesters)
        matchButton.place(x=700, y=560)
        
        # create the ListBox objects to display the country and device information
        Label(self, text="Select One or More Countries").place(x=20, y=0)
        self.countryListbox = Listbox(self, selectmode='multiple', height=20, width=25, exportselection=0)
        self.countryListbox.insert(1, "1")
        self.countryListbox.insert(2, "2")
        self.countryListbox.place(x=20, y=20)

        Label(self, text="Select One or More Devices").place(x=200, y=0)
        self.deviceListbox = Listbox(self, selectmode='multiple', height=20, width=30, exportselection=0)
        self.deviceListbox.place(x=200, y=20)
        self.deviceListbox.insert(1, "Samsung Galaxy S10")
        self.deviceListbox.insert(2, "iPhone 6S")

        Label(self, text="Tester Match Results:").place(x=450, y=0)
        self.resultsListbox = Listbox(self, height=20, width=30, exportselection=0)
        self.resultsListbox.place(x=450, y=20)
        scrollbar = Scrollbar(self, orient="vertical")
        scrollbar.config(command=self.resultsListbox.yview)
        scrollbar.place(x=632, y=22)
        scrollbar.pack(side="right", fill="y")
        self.resultsListbox.config(yscrollcommand=scrollbar.set)

        for i in range(100):
            self.resultsListbox.insert(END, "Line number " + str(i))

        # create another object to hold the output from the database query
        # this will show the results from the query or an 'error' message
        # if the user did not select at least one country and one device

    def matchTesters(self):
        selectedCountries = self.countryListbox.curselection()
        selectedDevices = self.deviceListbox.curselection()
        
        database.matchTesters()


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
    
    devicePicker = {}
    for device in allDevices:
        devicePicker[str(device[0])] = device[1].replace('\'','')

    root = Tk()
    root.geometry("800x600")
    app = Window(root)
    root.mainloop()


if __name__ == '__main__':
    main()
