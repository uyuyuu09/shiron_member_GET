import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
DEFAULT_API = os.getenv("DEFAULT_API")
GET_HUB = os.getenv("GET_HUB")
GET_MEMBER = os.getenv("GET_MEMBER")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
GOOGLE_AUTH_JSON = os.getenv('GOOGLE_AUTH_JSON')