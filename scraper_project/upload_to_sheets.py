import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "service_account.json", scope
)

client = gspread.authorize(creds)

sheet = client.open_by_url(
    "YOUR_GOOGLE_SHEET_URL"
).worksheet("Scraped Data")

df = pd.read_excel("output/data.xlsx")
sheet.clear()
sheet.update([df.columns.values.tolist()] + df.values.tolist())

print("✅ Uploaded to Google Sheets")
