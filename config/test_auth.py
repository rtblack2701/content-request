import os
import gspread
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
import json

# Force reload of environment variables
load_dotenv(override=True)

# Directly specify the new Sheet ID
SHEET_ID = "1UwrN8MqdmtzyRnORsSy9NcF0vOZOqdrGBTiFGstFAAk"  # New Sheet ID
CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")

print(f"Using Sheet ID: {SHEET_ID}")
print(f"Using Credentials Path: {CREDENTIALS_PATH}")

# Check if credentials file exists
if not os.path.exists(CREDENTIALS_PATH):
    print(f"Error: Credentials file not found at {CREDENTIALS_PATH}")
    exit(1)

# Define the scope
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

try:
    # Verify credentials file structure
    with open(CREDENTIALS_PATH, 'r') as f:
        creds_data = json.load(f)
        print(f"Credentials file loaded. Contains keys: {', '.join(creds_data.keys())}")
        print(f"Service account email: {creds_data.get('client_email', 'Not found')}")
    
    # Authenticate with the service account
    print("Attempting to authenticate...")
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, scope)
    print("Credentials loaded successfully")
    
    client = gspread.authorize(creds)
    print("Authorization successful")
    
    # Open the sheet by ID
    print(f"Attempting to open sheet with ID: {SHEET_ID}")
    sheet = client.open_by_key(SHEET_ID)
    print("Sheet opened successfully")
    
    worksheet = sheet.get_worksheet(0)  # First sheet (tab)
    print("Worksheet accessed successfully")
    
    # Fetch all records
    records = worksheet.get_all_records()
    print(f"Found {len(records)} records")
    
    if records:
        print("First record keys:", list(records[0].keys()))
    
except Exception as e:
    print(f"Error: {type(e).__name__}: {str(e)}")
