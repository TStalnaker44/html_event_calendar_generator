"""
Author: Trevor Stalnaker
File: calGenerator.py

Update the events.csv file located in the same directory
and run this script to generate a fully functional html
calendar that can be used on a website, including those
created using web building tools like Weebly.

The html is saved both to an external file (calendar.html)
and, if pyperclip is installed, to the user's clipboard.

Change the month and year constraints as needed.
"""

import resources.cal_utils as cal_utils

try:
    import pyperclip
    hasPyClip = True
except:
    hasPyClip = False

# Set Constants
MONTH = 10
YEAR = 2019

# Generate the HTML for the calendar
html = cal_utils.getHTML(MONTH, YEAR)

if hasPyClip: pyperclip.copy(html)
file = open("calendar.html", "w")
file.write(html)
file.close()
