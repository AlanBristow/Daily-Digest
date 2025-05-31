import base64
import os.path
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]

def get_credentials():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def send_email_via_gmail(creds, from_email, to_email, subject, body_text):
    """
    Send an email using Gmail API and OAuth2 credentials.
    """
    try:
        # Build the Gmail service
        service = build('gmail', 'v1', credentials=creds)

        # Create email message
        message = MIMEText(body_text)
        message['to'] = to_email
        message['subject'] = subject
        message['From'] = from_email

        # Encode message
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        body = {'raw': raw}

        # Send it
        sent_message = service.users().messages().send(userId="me", body=body).execute()
        print(f"✅ Email sent! ID: {sent_message['id']}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

def main():
    creds = get_credentials()
    to_email = "alan.m.bristow@gmail.com"
    subject = "Test Email"
    body_text = "This is a test email sent using the Gmail API."
    from_email = 'Daily Digest <alan.m.bristow@gmail.com>'
    print("Sending email...")
    send_email_via_gmail(creds, from_email, to_email, subject, body_text)
    print("Email sent successfully.")

if __name__ == '__main__':
    main()