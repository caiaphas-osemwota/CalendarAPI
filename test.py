from ics import Event #, Calendar
from dotenv import load_dotenv
from icalendar import Calendar
import requests
import os
import datetime
import arrow

load_dotenv()
url = os.getenv("copiedURL")
cal = Calendar.from_ical(requests.get(url).text) #parses url and converts to icalendar object
event_list = []

for event in cal.walk():
    if event.name == "VEVENT":
        eventstart = event.get("DTSTART").dt
        eventend = event.get("DTEND").dt
        event_list.append({
            'event_name' : str(event.get('SUMMARY')),
            'begin_event_time' : eventstart,
            'end_event_time' : eventend,
            'duration' : (eventend - eventstart).total_seconds()
                #can add more with dir(events_it)
        })
sorted_event_list = sorted(event_list, key=lambda event:event['begin_event_time'])
print(sorted_event_list)