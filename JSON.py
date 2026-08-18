#For future JSON loading and dumping 
import json
from main import sorted_event_list , study_block_list
JSON_event_list = [] 
for sorted_event in sorted_event_list:
    JSON_event_list.append({
        'event_name_JSON' : sorted_event['event_name'],
        'begin_event_timeISO' : sorted_event['begin_event_time'].isoformat(),
        'end_event_timeISO' : sorted_event['end_event_time'].isoformat()
    })
JSON_study_block_list = []
for JSONstudyblock in study_block_list:
    JSON_study_block_list.append({
        'assignment_name_JSON' : JSONstudyblock['assignment_name'],
        'studytimestartISO' : JSONstudyblock['study_time_start'].isoformat(),
        'studytimeendISO' : JSONstudyblock['study_time_end'].isoformat()
    })
with open('study_block_list.json', 'w') as f:
    Studying_JSON = json.dump(JSON_study_block_list, f, indent=4) 
with open("event_list.json", "w") as f:
    Classes_JSON = json.dump(JSON_event_list, f, indent=4)
#with open("event_list
#.json", "r") as f:
#    jsontolist = json.load(f)