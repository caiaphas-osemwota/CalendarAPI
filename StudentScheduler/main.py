from ics import Calendar
import requests
url = ("https://calendar.google.com/calendar/ical/cai.osemwota%40gmail.com/private-8be2b30d0af724314581cc7d08dcdc81/basic.ics")

cal = Calendar(requests.get(url).text) #reads url and translates to text
#events_it = next(iter(cal.events)) #gets one event from cal.events
#print(dir(events_it)) #looks at applicable methods/attributes
events = cal.events
dictonarylist = []
for event in events :
    dictionary = {
        'eventname' : event.name,
        'begindatetime' : event.begin,
        'enddatetime' : event.end,
        'duration' : event.duration
        #can add more with dir(events_it)
    }
    dictonarylist.append(dictionary)
#print(dictonarylist)
print(type(event.begin))
print(type(event.end))
print(type(event.duration))