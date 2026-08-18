from ics import Calendar, Event
from dotenv import load_dotenv
import requests
import os
import datetime
import arrow

load_dotenv()
url = os.getenv("copiedURL")
cal = Calendar(requests.get(url).text) #reads url and translates to text
Day_Start_Input = arrow.get(input("What time do you want to start your day? (input as XX:XX AM/PM)"), 'h:mm A' ) 
Day_End_Input = arrow.get(input("What time do you want to end your day? (input as XX:XX AM/PM)"), 'h:mm A' )
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

for i in range(0,len(sorted_event_list)-1):
    current_event = sorted_event_list[i]
    next_event = sorted_event_list[i+1]
    current_event_day = current_event['end_event_time'].replace(hour=0, minute=0, second=0, microsecond=0) #replace the event's time with 0
    Day_Start = current_event_day.shift(hours = Day_Start_Input.hour, minutes = Day_Start_Input.minute) #shift current event day by inputted time
    Day_End = current_event_day.shift(hours = Day_End_Input.hour, minutes = Day_End_Input.minute)
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
    if i == 0 :
        freetime = {
            'begin_freetime' : Day_Start,
            'end_freetime' : current_event['begin_event_time'],
            'freetime_duration' : current_event['begin_event_time'] - Day_Start
            }
    elif i == len(sorted_event_list)-2:
        freetime = {
            'begin_freetime' : current_event['end_event_time'],
            'end_freetime' : Day_End,
            'freetime_duration' : Day_End - current_event['end_event_time']
        }
    else:
        freetime = {
            'begin_freetime' : current_event['end_event_time'],
            'end_freetime' : next_event['begin_event_time'],
            'freetime_duration' : current_event['end_event_time'] - next_event['begin_event_time']
            }
    freetimebegin = next_event['end_event_time'] if i == len(sorted_event_list)-2
    freetimeend = Day_End if i == len(sorted_event_list)-2 else next_event['begin_event_time']
    if freetime['freetime_duration'].total_seconds() < 600:
        continue
    freetime_list.append(freetime)
study_block_list = []
freetime_index = 0
#MaxStudyBlockDuration = 7200 work on including breaks within study blocks
freetime_list_copy = [dict(f) for f in freetime_list] #copies and unravels freetime_list
for assignment in total_assignment_time_list :
    remaining_study_time = assignment['study_time']
    while remaining_study_time > 0 and freetime_index < len(freetime_list_copy):
        block = freetime_list_copy[freetime_index]
        block_duration = block['freetime_duration'].total_seconds()
        if block_duration <= 0:
            freetime_index += 1
            continue
        allotted = min(remaining_study_time, block_duration) #picks smaller one of either remaining study time or block duration
        study_block = {
            'study_name' : assignment['assignment_name'] + " " + "Study", #change naming later to get rid of the due
            'study_time_start' : block['begin_freetime'],
            'study_time_end' : block['begin_freetime'] + datetime.timedelta(seconds = allotted) #sets alloted time to timedelta to add to date object 'end_freetime'
            }
        study_block_list.append(study_block)
        remaining_study_time -= allotted
        block['begin_freetime'] = study_block['study_time_end']
        block['freetime_duration'] -= datetime.timedelta(seconds=allotted)
        if block['freetime_duration'].total_seconds() <= 0:
            freetime_index += 1
Schedule_Calendar = Calendar()
for each_block in study_block_list :
    Scheduled_Study_Blocks = Event()
    Scheduled_Study_Blocks.name = each_block['study_name']
    Scheduled_Study_Blocks.begin = each_block['study_time_start']
    Scheduled_Study_Blocks.end = each_block['study_time_end']
    Schedule_Calendar.events.add(Scheduled_Study_Blocks)
with open("my.ics", "w") as f:
    f.write(Schedule_Calendar.serialize())

#limit lookup to 5 months ahead
#maybe add meal times?
#MaxStudyBlockDuration = 7200
#MinStudyBlockDuration = 1800

print(f"Total events: {len(sorted_event_list)}")
print(f"Free time gaps found: {len(freetime_list)}")
print(f"Assignments found: {len(total_assignment_time_list)}")