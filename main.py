from ics import Calendar
from dotenv import load_dotenv
import requests
import os
import json
load_dotenv()
url = os.getenv("copiedURL")
cal = Calendar(requests.get(url).text) #reads url and translates to text
#events_it = next(iter(cal.events)) #gets one event from cal.events
#print(dir(events_it)) #looks at applicable methods/attributes
events = cal.events
dictionarylist = []
for event in events :
    dictionary = {
        'eventname' : event.name,
        'begineventtime' : event.begin,
        'endeventtime' : event.end,
        'duration' : event.duration.total_seconds()
        #can add more with dir(events_it)
    }
    dictionarylist.append(dictionary)
sorteddictionarylist = sorted(dictionarylist, key=lambda event:event['begineventtime'])

assignmentlist = []
freetimelist = [] 
for i in range(0,len(sorteddictionarylist)-1):
    currentevent = sorteddictionarylist[i]
    nextevent = sorteddictionarylist[i+1] 
    Freetime = {
        'beginfreetime' : currentevent['endeventtime'],
        'endfreetime' : nextevent['begineventtime'],
    }
    FreetimeGap = (Freetime['endfreetime'] - Freetime['beginfreetime'])
    if FreetimeGap.total_seconds() < 600:
        continue
    freetimelist.append(Freetime)
    if "due" in currentevent['eventname']:
        assignments = {
            'assignmentname' : currentevent['eventname'],
            'assignmentduedatetime' : currentevent['endeventtime']
            }
        assignmentlist.append(assignments)



#DayStart = input("What time do you want to start your day? (input as XX:XX)") #change later
#DayEnd = input("What time do you want to end your day? (input as XX:XX)") #change later
#limit lookup to 5 months ahead
#maybe add meal times?
#MaxStudyBlockDuration = 7200
#MinStudyBlockDuration = 1800

#print(freetimelist)

JSONdictionarylist = []
for event in events :
    ISOdictionary = {
        'eventnameJSON' : event.name,
        'begineventtimeISO' : event.begin.isoformat(),
        'endeventtimeISO' : event.end.isoformat()
    }
    JSONdictionarylist.append(ISOdictionary)
sortedJSONdictlist = sorted(JSONdictionarylist, key=lambda event:event['begineventtimeISO'])
with open("dictionarylist.json", "w") as f:
    ClassesJson = json.dump(sortedJSONdictlist, f, indent=4) # get rid of indent later on (only for readability)
#with open("dictionarylist.json", "r") as f:
#    jsontolist = json.load(f)
print(f"Total events: {len(sorteddictionarylist)}")
print(f"Free time gaps found: {len(freetimelist)}")
print(f"Assignments found: {len(assignmentlist)}")