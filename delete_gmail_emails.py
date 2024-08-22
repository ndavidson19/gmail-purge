import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def delete_message(service, msg_id):
    try:
        service.users().messages().delete(userId='me', id=msg_id).execute()
        print(f'Message with ID: {msg_id} deleted successfully.')
    except Exception as e:
        print(f'An error occurred: {e}')

def main():
    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)

    # Load emails to delete from the JSON file
    with open('emails_to_delete.json', 'r') as f:
        emails_to_delete = json.load(f)

    print(f'Deleting {len(emails_to_delete)} emails...')
    
    for email in emails_to_delete:
        delete_message(service, email['id'])

    print('Cleanup completed.')

if __name__ == '__main__':
    main()
