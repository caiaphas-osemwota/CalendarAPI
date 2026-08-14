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
event_list = []
for event in events :
    event_list.append({
        'event_name' : event.name,
        'begin_event_time' : event.begin,
        'end_event_time' : event.end,
        'duration' : event.duration.total_seconds()
        #can add more with dir(events_it)
    })
sorted_event_list = sorted(event_list, key=lambda event:event['begin_event_time'])

total_assignment_time_list = []
freetime_list = []
study_time_list = [] 
for i in range(0,len(sorted_event_list)-1):
    current_event = sorted_event_list[i]
    next_event = sorted_event_list[i+1]
    study_time = 0 
    if "due" in current_event['event_name'].lower():
         current_assignment = current_event['event_name']
         assignment_text = current_assignment.lower()
         keyword_times = {
                    'calc' : 7200,
                    'physics' : 3600,
                    'programming' : 9000,
                    'linear' : 2700
                    }
         for keyword, time in keyword_times.items(): #unravels tuple and makes first item the keyword and its assigned value the time
            if keyword in assignment_text:
                study_time += time
         assignment_dict = {
            'assignment_name' : current_event['event_name'],
            'assignment_due_date_time' : current_event['begin_event_time'],
            'study_time' : study_time
            }
         total_assignment_time_list.append(assignment_dict)

    freetime = {
        'beginfreetime' : current_event['end_event_time'],
        'endfreetime' : next_event['begin_event_time'],
    }
    freetime_gap = (freetime['endfreetime'] - freetime['beginfreetime'])
    if freetime_gap.total_seconds() < 600:
        continue
    freetime_list.append(freetime)

#DayStart = input("What time do you want to start your day? (input as XX:XX)") #change later
#DayEnd = input("What time do you want to end your day? (input as XX:XX)") #change later
#limit lookup to 5 months ahead
#maybe add meal times?
#MaxStudyBlockDuration = 7200
#MinStudyBlockDuration = 1800

#Scheduler


JSON_event_list = [] #look into pulling sorted dictionary list and 
for event in events :
    ISOdictionary = {
        'eventnameJSON' : event.name,
        'begineventtimeISO' : event.begin.isoformat(),
        'end_event_timeISO' : event.end.isoformat()
    }
    JSON_event_list.append(ISOdictionary)
sorted_JSON_dict_list = sorted(JSON_event_list, key=lambda event:event['begineventtimeISO'])
with open("event_list.json", "w") as f:
    ClassesJson = json.dump(sorted_JSON_dict_list, f, indent=4) # get rid of indent later on (only for readability)
#with open("event_list
#.json", "r") as f:
#    jsontolist = json.load(f)
print(f"Total events: {len(sorted_event_list)}")
print(f"Free time gaps found: {len(freetime_list)}")
print(f"Assignments found: {len(total_assignment_time_list)}")