from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime
import pytz

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def get_drive_service():
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
    return build('drive', 'v3', credentials=creds)

def list_files(service):
    results = service.files().list(
        pageSize=1000, fields="nextPageToken, files(id, name, mimeType, size, modifiedTime)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            size = int(item.get('size', 0))
            modified_time = datetime.fromisoformat(item['modifiedTime'].replace('Z', '+00:00'))
            print(f"{item['name']} ({size/1024/1024:.2f} MB) - Last modified: {modified_time}")
    return items

def sort_files(files, sort_by='size'):
    if sort_by == 'size':
        return sorted(files, key=lambda x: int(x.get('size', 0)), reverse=True)
    elif sort_by == 'date':
        return sorted(files, key=lambda x: x['modifiedTime'], reverse=True)

def delete_file(service, file_id):
    try:
        service.files().delete(fileId=file_id).execute()
        print(f"File with id {file_id} deleted successfully.")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def main():
    service = get_drive_service()
    files = list_files(service)
    
    while True:
        print("\nGoogle Drive Manager")
        print("1. List top 10 largest files")
        print("2. List 10 most recently modified files")
        print("3. Delete large files")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            print("\nTop 10 largest files:")
            for file in sort_files(files, 'size')[:10]:
                size = int(file.get('size', 0))
                print(f"{file['name']} ({size/1024/1024:.2f} MB)")
        
        elif choice == '2':
            print("\nMost recently modified files:")
            for file in sort_files(files, 'date')[:10]:
                modified_time = datetime.fromisoformat(file['modifiedTime'].replace('Z', '+00:00'))
                print(f"{file['name']} - Last modified: {modified_time}")
        
        elif choice == '3':
            size_threshold = float(input("Enter size threshold in MB: ")) * 1024 * 1024  # Convert MB to bytes
            large_files = [file for file in sort_files(files, 'size') if int(file.get('size', 0)) > size_threshold]
            
            if not large_files:
                print(f"No files larger than {size_threshold/1024/1024} MB found.")
                continue

            print(f"\nFiles larger than {size_threshold/1024/1024} MB:")
            for file in large_files:
                size = int(file.get('size', 0))
                print(f"{file['name']} ({size/1024/1024:.2f} MB)")

            confirm = input("Do you want to delete these files? (yes/no): ").lower()
            
            if confirm == 'yes':
                for file in large_files:
                    if delete_file(service, file['id']):
                        print(f"Deleted: {file['name']} ({int(file.get('size', 0))/1024/1024:.2f} MB)")
                    else:
                        print(f"Failed to delete: {file['name']}")
                # Refresh the file list after deletions
                files = list_files(service)
            else:
                print("Operation cancelled. No files were deleted.")
        
        elif choice == '4':
            print("Exiting Google Drive Manager. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()