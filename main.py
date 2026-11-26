from ics import Event, Calendar as IcsCalendar
from dotenv import load_dotenv
from icalendar import Calendar
import requests
import os
import datetime
from datetime import timedelta
from zoneinfo import ZoneInfo

Local_TZ = ZoneInfo("America/Indiana/Indianapolis")

def to_local(value): # all-day events are just normal dates, floating times have no timezone
    if not isinstance(value, datetime.datetime):
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=LOCAL_TZ)
    return value.astimezone(LOCAL_TZ)

load_dotenv()
lecture_url = os.getenv("copiedURL")
assigmnent_url = os.getenv("copiedURL2")
cal1 = Calendar.from_ical(requests.get(lecture_url).content) #parses lecture_url and converts to icalendar object
cal2 = Calendar.from_ical(requests.get(assigmnent_url).content) #parses assignment_url and converts to icalendar object
Day_Start_User_Input = input("What time do you want to start your day? (input as XX:XX AM/PM) ")
Day_End_User_Input = input("What time do you want to end your day? (input as XX:XX AM/PM) ")
try:
    Day_Start_Input = datetime.datetime.strptime(Day_Start_User_Input, '%I:%M %p' )
    Day_End_Input = datetime.datetime.strptime(Day_End_User_Input, '%I:%M %p' )
except ValueError:
    print("Incorrect time format, should be HH:MM AM/PM")
    exit()
event_list = []
homework_list = []
for event in cal1.walk():
    if event.name == "VEVENT":
        eventstart = to_local(event.get("DTSTART").dt) 
        if eventstart is None:
            continue
        eventend = to_local(event.get("DTEND").dt) if event.get("DTEND") else eventstart
        event_list.append({
            'event_name' : str(event.get('SUMMARY')),
            'begin_event_time' : eventstart,
            'end_event_time' : eventend,
            'duration' : (eventend - eventstart).total_seconds()
                #can add more with dir(events_it)
        })
sorted_event_list = sorted(event_list, key=lambda event:event['begin_event_time'])

for homework in cal2.walk():
    if homework.name == "VEVENT":
        homeworkstart = to_local(homework.get("DTSTART").dt)
        if homeworkstart is None:
            continue
        homeworkend = to_local(homework.get("DTEND").dt) if homework.get("DTEND") else homeworkstart
        homework_list.append({
            'homework_name' : str(homework.get('SUMMARY')),
            'homework_description' : str(homework.get('DESCRIPTION')),
            'begin_homework_time' : homeworkstart,
            'end_homework_time' : homeworkend,
            'duration' : (homeworkend - homeworkstart).total_seconds()
                #can add more with dir(events_it)
        })
sorted_homework_list = sorted(homework_list, key=lambda homework:homework['begin_homework_time'])

total_assignment_time_list = []
freetime_list = []

for i in range(0,len(sorted_event_list)-1):
    current_event = sorted_event_list[i]
    next_event = sorted_event_list[i+1]
    current_event_day = current_event['end_event_time'].replace(hour=0, minute=0, second=0) #replace the event's time with 0
    Day_Start = current_event_day + timedelta(hours = Day_Start_Input.hour, minutes = Day_Start_Input.minute) #shift current event day by inputted time
    Day_End = current_event_day + timedelta(hours = Day_End_Input.hour, minutes = Day_End_Input.minute)
    if i == 0 :
        freetime = {
            'begin_freetime' : Day_Start,
            'end_freetime' : current_event['begin_event_time'],
            'freetime_duration' : current_event['begin_event_time'] - Day_Start
            }
    elif i == len(sorted_event_list)-2:
        freetime = {
            'begin_freetime' : next_event['end_event_time'],
            'end_freetime' : Day_End,
            'freetime_duration' : Day_End - next_event['end_event_time']
        }
    else:
        freetime = {
            'begin_freetime' : current_event['end_event_time'],
            'end_freetime' : next_event['begin_event_time'],
            'freetime_duration' : next_event['begin_event_time'] - current_event['end_event_time']
            }
    if freetime['freetime_duration'].total_seconds() < 600:
        continue
    freetime_list.append(freetime)
for i in range(0,len(sorted_homework_list)):
    study_time = 0 
    if "due" in sorted_homework_list[i]['homework_name'].lower():
            current_assignment_class_name = sorted_homework_list[i]['homework_description']
            current_assignment_name = sorted_homework_list[i]['homework_name']
            assignment_text = current_assignment_class_name.lower()
            keyword_times = {
                        'ma 261' : 7200,
                        'phys 251' : 3600,
                        'ece 229' : 9000,
                        'ece 201' : 2700
                        }
            for keyword, time in keyword_times.items(): #unravels tuple and makes first item the keyword and its assigned value the time
                if keyword in assignment_text:
                    study_time += time
            assignment_dict = {
                'assignment_name' : current_assignment_name,
                'assignment_due_date_time' : sorted_homework_list[i]['end_homework_time'],
                'study_time' : study_time
                }
            total_assignment_time_list.append(assignment_dict)
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

#maybe add meal times?
#MaxStudyBlockDuration = 7200
#MinStudyBlockDuration = 1800

print(f"Total events: {len(sorted_event_list)}")
print(f"Free time gaps found: {len(freetime_list)}")
print(f"Assignments found: {len(total_assignment_time_list)}")