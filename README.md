# Gmail Cleanup Script

UCLA is shutting down our Google accounts if we do not maintain our total storage under 5 GB. This repository contains Python scripts to help you manage your Gmail storage by identifying and deleting large, old, and spam emails. If you find yourself in a similar situation, these scripts can assist you in staying under the storage limit.

There is an additional script `delete_drive.py` which as it sounds like deletes your google drive files. This is useful if you have a lot of files in your google drive that you don't need anymore, but most likely you will need to modify the script to fit your needs. For our use-case they turned off our access to drive and we were unable to delete files through the web interface giving us no choice but to purge it for extra space.

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

If you are using the `delete_drive.py` script you will also need to install the following:
```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client pytz
```

### Step 3: Create an environment file and edit the configuration
If you choose to use whitelisted emails that you do not want to delete, please add them to an .env file in the root directory of the project. The .env file should contain the following variables:

```bash
WHITELISTED_EMAILS=""
```

Similarly, if you would like to mark any emails as spam that you do not want to delete, please add them to list in the `list_gmail_emails.py` script. TODO: Add support for an environment variable. 

### Step 4: Run the Scripts
The listing script identifies emails that can be deleted and generates a JSON file for review:
```bash
python list_gmail_emails.py
```
This will create two files:
- `emails_to_delete.json`: Contains the list of emails identified for deletion.
- `deletion_stats.txt`: Contains statistics about the emails that are going to be deleted, including total size and breakdown by category (spam, large, old emails).

If you are using the `delete_drive.py` script you will need to run the following command:
```bash
python delete_drive.py
```

### Step 5: Review Emails
Open the `emails_to_delete.json` file to review the emails that will be deleted. You can modify this file to exclude specific emails from deletion.

### Step 6: Delete Emails
Once you've reviewed the emails, you can delete them using the following script:

```bash
python delete_gmail_emails.py
```

Please note that this script will permanently delete the emails. There is no way to recover them once they are deleted. It also takes orders of magnitude longer to delete the emails than to compile the list, so be patient and let the script run to completion. If you are unsatisfied with Python's speed in loops then I emplore you to write it in Rust or try to turn this into multiple threads.

## Notes

- The scripts are designed to be as safe as possible by separating the listing and deletion steps. Always review the emails_to_delete.json file before running the deletion script.
- The deletion script will permanently delete the emails. There is no way to recover them once they are deleted.
- Depending on the number of emails to be deleted, the deletion process may take some time. Be patient and let the script run to completion. TODO: Add progress indicator.

## Contributing
If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

---
This project was created out of necessity due to UCLA's storage limitations on Google accounts. We hope it helps others who may be in similar situations.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
