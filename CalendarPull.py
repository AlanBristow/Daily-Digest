from __future__ import print_function
import os.path
import datetime
import pickle  # to save credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these scopes, delete the token.pickle file first
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    creds = None
    # Load credentials if they exist
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials available, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # 🔥 this refreshes the token
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Build the calendar service
    service = build('calendar', 'v3', credentials=creds)

    # Get upcoming 10 events
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(
        calendarId='primary', timeMin=now,
        maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

if __name__ == '__main__':
    main()
