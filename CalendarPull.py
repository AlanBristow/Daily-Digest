from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from datetime import timezone

def get_today_events(creds):
    service = build('calendar', 'v3', credentials=creds)

    # Get the current date in UTC
    today = datetime.datetime.utcnow().date()

    # List all calendars
    calendar_list = service.calendarList().list().execute()
    calendar_ids = [cal['id'] for cal in calendar_list['items']]

    # Fetch events for the current day from each calendar
    all_events = []
    for cal_id in calendar_ids:
        try:
            events_result = service.events().list(
                calendarId=cal_id,
                timeMin=today.isoformat() + 'T00:00:00Z',
                timeMax=today.isoformat() + 'T23:59:59Z',
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            all_events.extend(events_result.get('items', []))
        except Exception as e:
            print(f"Error fetching from calendar {cal_id}: {e}")

    # Filter events to ensure they match today's date
    filtered_events = []
    for event in all_events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        event_date = datetime.datetime.strptime(start.split('T')[0], '%Y-%m-%d').date()
        if event_date == today:
            filtered_events.append(event)

    # Sort events by start time
    filtered_events.sort(key=lambda x: x['start'].get('dateTime', x['start'].get('date')))

    # Format events for display
    formatted_events = []
    for event in filtered_events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        summary = event.get('summary', '(No title)')

        if 'dateTime' in event['start']:
            start_dt = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z')
            end_dt = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%S%z')
            start_formatted = start_dt.strftime('%d/%m/%Y %I:%M%p')
            end_formatted = end_dt.strftime('%I:%M%p')
            formatted_events.append(f"{start_formatted} - {end_formatted} : {summary}")
        else:  # All-day event
            start_dt = datetime.datetime.strptime(start, '%Y-%m-%d')
            start_formatted = start_dt.strftime('%d/%m/%Y')
            formatted_events.append(f"{start_formatted} : {summary}")

    return formatted_events