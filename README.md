# CalendarAPI

A Python-based study scheduling system that reads calendar events, identifies available time, and automatically schedules study blocks around a student's academic workload.

## Background

I came up with the idea while writing my own schedule before starting college, and challenged myself to turn it into a working program before classes began. The project has since become a way to practice Python, APIs, data structures, datetime handling, file generation, and scheduling algorithms.

## Current Functionality

- Reads calendar events from an iCalendar URL
- Converts calendar events into structured Python dictionaries
- Sorts events chronologically
- Accepts a user-defined start and end time for each day
- Identifies free time between scheduled events
- Detects assignments based on calendar event names containing "due"
- Estimates study time based on course keywords
- Supports different study-time allocations for Calculus, Physics, Programming, and Linear Circuits
- Filters out free-time gaps shorter than 10 minutes
- Allocates required study time across available free-time blocks
- Splits assignments across multiple free-time periods when needed
- Tracks remaining availability as study blocks are scheduled
- Generates a new `.ics` calendar containing scheduled study blocks
- Prints scheduling statistics, including total events, free-time gaps, and assignments found

## Current Workflow
Calendar URL
↓
Read Calendar Events
↓
Sort Events
↓
Identify Assignments
↓
Find Free Time
↓
Estimate Required Study Time
↓
Schedule Study Blocks
↓
Generate .ics Calendar

## Technologies

- Python
- ics
- Requests
- python-dotenv
- Arrow
- iCalendar
- Git / GitHub

## Future Improvements

- Improve assignment detection accuracy
- Add configurable study durations
- Add maximum study block lengths
- Add scheduled breaks
- Improve study block prioritization
- Support more courses and assignment types (e.g., exam and test prep)
- Automatically update the generated calendar
- Host the generated `.ics` feed for calendar subscriptions
- Add a user interface for scheduling preferences
