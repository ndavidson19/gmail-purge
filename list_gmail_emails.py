import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

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

def list_messages(service, query=''):
    try:
        response = service.users().messages().list(userId='me', q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])
        return messages
    except Exception as e:
        print(f'An error occurred: {e}')
        return []

def get_email_details(service, message_ids):
    email_details = []
    total_size = 0
    for email in message_ids:
        message = service.users().messages().get(userId='me', id=email['id']).execute()
        size = message.get('sizeEstimate', 0)
        total_size += size
        from_email = next(header['value'] for header in message['payload']['headers'] if header['name'] == 'From')
        email_details.append({
            'id': email['id'],
            'snippet': message['snippet'],
            'size': size,
            'from': from_email
        })
    return email_details, total_size

def filter_whitelist(emails):
    whitelist = set(os.getenv('WHITELISTED_EMAILS', '').split(','))
    filtered_emails = [email for email in emails if not any(whitelisted in email['from'] for whitelisted in whitelist)]
    return filtered_emails

def main():
    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)

    # Define the list of sender emails to target as spam
    spam_senders = [
        "jobs-listings@linkedin.com",
        "jobalerts-noreply@linkedin.com",
        "team@datacamp.com",
        "newsletters@biospace.com",
        "FromYouFlowers@email.fromyouflowers.com",
        "newsletters@medium.com",
        "biospace_noreply@biospace.com",
        "jobs@alerts.jobot.com",
        "alert@notification.bebee.com"
    ]

    # Search for emails from spam senders
    spam_emails = []
    for sender in spam_senders:
        query = f"from:{sender}"
        spam_emails.extend(list_messages(service, query))
    spam_details, spam_total_size = get_email_details(service, spam_emails)
    print(f'Found {len(spam_emails)} emails from spam senders.')

    # Search for large emails
    large_emails = list_messages(service, 'larger:5M')
    large_details, large_total_size = get_email_details(service, large_emails)
    print(f'Found {len(large_emails)} large emails.')

    # Search for old emails
    old_emails = list_messages(service, 'older_than:2y')
    old_details, old_total_size = get_email_details(service, old_emails)
    print(f'Found {len(old_emails)} emails older than 2 years.')

    # Combine all details
    emails_to_delete = spam_details + large_details + old_details

    # Filter out whitelisted emails
    emails_to_delete = filter_whitelist(emails_to_delete)

    # Save the email details to a JSON file
    with open('emails_to_delete.json', 'w') as f:
        json.dump(emails_to_delete, f, indent=2)

    # Calculate total size to be deleted
    total_size = sum(email['size'] for email in emails_to_delete)

    # Output statistics to a text file
    with open('deletion_stats.txt', 'w') as f:
        f.write("Deletion Statistics:\n")
        f.write("====================\n\n")
        f.write(f"Total emails to be deleted: {len(emails_to_delete)}\n")
        f.write(f"Total size to be deleted: {total_size / (1024 * 1024):.2f} MB\n\n")

        f.write("Breakdown by Category:\n")
        f.write("----------------------\n")
        f.write(f"Spam emails:\n")
        f.write(f"  Number: {len(spam_details)}\n")
        f.write(f"  Size: {spam_total_size / (1024 * 1024):.2f} MB\n\n")

        f.write(f"Large emails:\n")
        f.write(f"  Number: {len(large_details)}\n")
        f.write(f"  Size: {large_total_size / (1024 * 1024):.2f} MB\n\n")

        f.write(f"Old emails:\n")
        f.write(f"  Number: {len(old_details)}\n")
        f.write(f"  Size: {old_total_size / (1024 * 1024):.2f} MB\n\n")

    print(f'Deletion statistics saved to deletion_stats.txt.')
    print(f'{len(emails_to_delete)} emails saved to emails_to_delete.json for review.')

if __name__ == '__main__':
    main()
