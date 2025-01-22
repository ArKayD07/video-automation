from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import openai
import gspread
from oauth2client.service_account import ServiceAccountCredentials

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("path/to/your/credentials.json", scope)
client = gspread.authorize(creds)

spreadsheet = client.open("Video Automation System")
sheet = spreadsheet.sheet1
first_cell_value = sheet.cell(1, 1).value

print(f"The value of the first cell is: {first_cell_value}")