import os
import gspread
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import typer

load_dotenv()

SHEET_ID = os.getenv("SHEET_ID")

def log_form_response():
    if not latest:
        return None
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "latest_form_response.log")

    with open(log_path, "w") as f:
        f.write(f"✅ Latest Form Response - Logged at {datetime.datetime.now()}\n\n")
        for key, value in latest.items():
            f.write(f"{key}: {value}\n")

    return log_path

# Define the scope
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Authenticate with the service account
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Open the sheet by ID
sheet = client.open_by_key(SHEET_ID)
worksheet = sheet.get_worksheet(0)  # First sheet (tab)

# Fetch all records
records = worksheet.get_all_records()
latest = records[-1] if records else None

if not latest:
    print("No form responses found.")
else:
    path = log_form_response()
    typer.echo(f"✅ Form response logged to: {path}")

if __name__ == "__main__":
    if not latest:
        print("❌ No form responses found.")
    else:
        print("✅ Latest Form Response:")
        for key, value in latest.items():
            print(f"{key}: {value}")