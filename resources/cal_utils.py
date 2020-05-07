"""
Author: Trevor Stalnaker
File: cal_utils.py
"""

import random, csv, re
import calendar



def getCalendar(month, year):
    """
    Creates and returns an html calendar for the specified month
    and year
    """
    
    # Create a calendar object 
    cal = calendar.HTMLCalendar()

    # Set the beginning of the week to Sunday
    cal.setfirstweekday(6)

    # Create the calendar for the given month
    cal = cal.formatmonth(year, month, withyear=False)

    return cal


def getEventData():
    """
    Reads in event data from events.csv and returns it as a dictionary
    """
    dates = {}
    # Read event data from associated csv file
    with open('events.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            if row[0] != "Event Title":
                title = row[0]
                day   = row[1]
                time  = row[2]
                place = row[3]
                if day in dates.keys():
                    dates[day].append([title, time, place])
                else:
                    dates[day] = [[title, time, place]]   
    return dates


def getFile(fileName):
    """
    Helper function for opening and reading files and storing the
    result in a string
    """
    with open(fileName, 'r') as file:
        return file.read()


def getStyling():
    """
    Read in and return the external style sheet
    """
    return getFile('resources/css.txt')


def getScript():
    """
    Read in and return the external javascript
    """
    return getFile('resources/script.txt')


def createPTagWithID(ID):
    """
    Return a paragraph tag with a given ID
    """
    return "<p id=\"" + ID + "\"></p>"


def createDiv(ID, children):
    """
    Create a div with the provided ID and the provided
    elements nested within it
    """
    retString = "<div id=\"" + ID + "\">"
    for child in children:
        retString += child
    retString += "</div>"
    return retString


def increaseHeaderFont(html, size):
    """
    Increases the font size of the month header of the calendar
    """
    # Increase the font size of the header element (month)
    header, month = getMonthHeader(html, True)
    rep = "<th colspan=\"7\" class=\"month\" style=\"font-size:" + str(size) + "pt;\">" + \
          month + "</th>"
    return html.replace(header, rep)


def getMonthHeader(html, getHeader=False):
    """
    Returns the month and can also return the header holding it
    """
    header = re.search("\<th colspan=\"7\" class=\"month\"\>([A-Za-z]+)\</th\>", html).group(0)
    month = re.search("\<th colspan=\"7\" class=\"month\"\>([A-Za-z]+)\</th\>", html).group(1)
    if getHeader:
        return (header, month)
    else:
        return month


def addEventsToCalendar(html, month, dates):
    """
    Adds events to the calendar
    """
    tdRegex = re.compile(r'\<td class=\"[a-z]+\"\>')
    m = re.findall(tdRegex, html)
    for td in m:
        if td != "<td class=\"noday\">":
            date = re.search(re.compile("(?<=" + td + ")([\d]+)"), html).group(0)
            iD = generateRandomID()
            inlineStyle = ""
            clickText = ""
            if date in dates.keys():
                lyst = dates[date]
                txt, place, time = [],[],[]
                for event in lyst:
                    txt.append(event[0])
                    time.append(event[1])
                    place.append(event[2])
                inlineStyle = "style=\"font-weight:bold; font-size:14pt;\""
                for x in range(len(txt)):
                    clickText += "<br>"
                    clickText += "<p>" + txt[x] + "</p>"
                    clickText += "<p>" + time[x] + "</p>"
                    clickText += "<p>" + place[x] + "</p>"
                    #if x != len(txt)-1:
                    #    clickText += "<br>"
            else:
                txt = ["No Event Scheduled"]
            mouseOverText = "<br>".join(txt)
            events = "onmouseover=\"mouseOver('" + iD + \
                     "', '" + mouseOverText + "')\" onmouseout=\"mouseOut('" + iD + "')\"" + \
                     " onclick=\"onClick('" + clickText + "', '" + month + "', '" + date + "')\""
            replacement = td[:-1] + " id=\"" + iD + "\" " + inlineStyle + \
                            " " + events + ">" 
            html = html.replace(td, replacement, 1)
    return html


def generateRandomID(precision=8):
    """
    Generate a random id for an html element
    """
    ID = ""
    for x in range(precision):
        ID += chr(random.randint(97,122))
    return ID


def getHTML(month, year):
    """
    Returns the html for the page
    """

    # Create a dictionary which holds event information
    dates = getEventData()
    
    # Read in the external style sheet
    css = getStyling()

    # Read in the external javascript
    script = getScript()

    # Get the html for the calendar            
    cal = getCalendar(month, year)

    inspect = "<h2>Click the Calendar to See Events</h2>"

    # Create paragraphs to display event information
    paragraphs = []
    for p in ["event","billboard"]:
        paragraphs.append(createPTagWithID(p))

    eventDiv = "<div id=eventpara></div>"
        
    rightDiv = createDiv("right", [cal, paragraphs[0]])
    leftDiv  = createDiv("left", [inspect] + paragraphs[1:] + [eventDiv])

    container = "<div id=\"container\">" + rightDiv + leftDiv + "</div>"

    html = "<html><head></head><body>" + css + container + script + "</body></html>"
    html = increaseHeaderFont(html, 18)
    return addEventsToCalendar(html, calendar.month_name[month], dates)
