# Tester Matcher #

This simple application matches testers based on the input provided by the user.  

## Setup ##
1. Install Python 3.7+
    - This was tested on Python 3.7.4
2. Clone the repository:
    - ```git clone https://github.com/adaehling/TesterMatcher.git```
3. Change directories into the cloned repository
    - ```cd TesterMatcher```
4. Run the application by invoking ```tester_matcher.py``` with Python:
    - ```py .\tester_matcher.py```

## How To Use ##
The simple UI that appears was built with Tkinter. There are three main text areas in the application.  
The first area is the Country selection. The second is the Device selection. The third shows the matched testers.  

You are able to have multiple selections in each input area by clicking on each individual row. You deselect by clicking on the highlighted row.  

When you are done making selections, click the 'Match Testers' button to show the results.

---

## PowerShell script ##
This assignment was also completed by writing a small PowerShell script: Match-Tester.ps1.  
The script was developed on a Windows 10 machine with Powershell 5.1 (Windows Management Framework 5.1)  
However, the script should function as long as you have PowerShell 3 or higher. 

In a PowerShell prompt, invoke the script by calling ```.\Match-Tester.ps1```  
This bring up a simple Windows form with options to select countries and devices.  
After the selection is made click the 'Enter' button to match the testers.  
The results are printed to the terminal.

---

## Thoughts / Improvements ##
1. Using the in-memory SQLite database was to get around the requirement for the user to install SQLite on their own machine. 
2. The User Interface is not that great at all. My preference would be to use a real frontend framework and not have to use python libraries such as Tkinter or Pygame.
3. No testing was done, but using a framework like unittest would help solidify each function defined in the Python files.
4. There is a lack of user input sanitization and error handling that would be required in a more developed application.