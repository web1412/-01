import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Load credentials from GitHub secret
creds_json = os.environ['GOOGLE_SHEETS_CREDENTIALS']
creds_dict = json.loads(creds_json)
creds = Credentials.from_service_account_info(creds_dict)

# Set up the Sheets API
SHEET_ID = os.environ['SHEET_ID']
service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SHEET_ID, range='A2:D').execute()
values = result.get('values', [])

print(f"Retrieved {len(values)} rows from Google Sheets")

# Transform the data into a JavaScript array
products_js = "const products = " + json.dumps([
    {
        "name": row[0],
        "image": row[1],
        "price": float(row[2]) if row[2] and row[2].replace('.', '').isdigit() else 0,
        "description": row[3] if len(row) > 3 else ""
    } for row in values if len(row) > 2
], ensure_ascii=False)

print(f"Transformed {len(json.loads(products_js[18:]))} products")

# Write to products.js
with open('products.js', 'w', encoding='utf-8') as f:
    f.write(products_js)

print("Updated products.js successfully")