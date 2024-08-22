# Gmail Cleanup Script

UCLA is shutting down our Google accounts if we do not maintain our total storage under 5 GB. This repository contains Python scripts to help you manage your Gmail storage by identifying and deleting large, old, and spam emails. If you find yourself in a similar situation, these scripts can assist you in staying under the storage limit.

## Features

- **List Emails for Deletion**: Identify emails that can be deleted, including large emails, old emails, and spam emails from specific senders.
- **Calculate Deletion Statistics**: Provides a breakdown of the potential storage savings from deleting these emails.
- **Safe Review Before Deletion**: Allows you to review emails in a JSON file before deletion.
- **Delete Emails**: A separate script to delete the identified emails after review.

## Prerequisites

- Python 3.x
- Google Gmail API credentials

## Setup Instructions

### Step 1: Clone the Repository

```bash
git clone https://github.com/ndavidson19/gmail-purge.git
cd gmail-purge
```

### Step 2: Install Required Libraries

To use these scripts, you need to set up a Google Cloud project and obtain the necessary credentials.

1. Create a Google Cloud Project:
- Go to the [Google Cloud Console](https://console.cloud.google.com/).
- Click on "Select a project" and then "New Project".
- Give your project a name and create it.

2. Enable the Gmail API:
- Go to the [APIs & Services Dashboard](https://console.cloud.google.com/apis/dashboard).
- Click on "Enable APIs and Services".
- Search for "Gmail API" and click on it.
- Click on "Enable".

3. Create Credentials:
- Go to the [APIs & Services Credentials page](https://console.cloud.google.com/apis/credentials).
- Click on "Create Credentials" and select "OAuth 2.0 Client IDs".
- Choose "Desktop app" as the application type.
- Click on "Create" and download the credentials JSON file and place in the root directory of the clone project repository.

4. Install Required Libraries:
```bash
pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Step 3: Run the Scripts
The listing script identifies emails that can be deleted and generates a JSON file for review:
```bash
python list_gmail_emails.py
```
This will create two files:
- `emails_to_delete.json`: Contains the list of emails identified for deletion.
- `deletion_stats.txt`: Contains statistics about the emails that are going to be deleted, including total size and breakdown by category (spam, large, old emails).

### Step 4: Review Emails
Open the `emails_to_delete.json` file to review the emails that will be deleted. You can modify this file to exclude specific emails from deletion.

### Step 5: Delete Emails
Once you've reviewed the emails, you can delete them using the following script:

```bash
python delete_gmail_emails.py
```

## Notes

- The scripts are designed to be as safe as possible by separating the listing and deletion steps. Always review the emails_to_delete.json file before running the deletion script.
- The deletion script will permanently delete the emails. There is no way to recover them once they are deleted.

## Contributing
If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

---
This project was created out of necessity due to UCLA's storage limitations on Google accounts. We hope it helps others who may be in similar situations.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
