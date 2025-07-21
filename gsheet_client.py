import os
import base64
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_gspread_client():
    encoded_key = os.environ.get("SERVICE_ACCOUNT_BASE64")
    if not encoded_key:
        raise Exception("환경변수 'SERVICE_ACCOUNT_BASE64'가 설정되지 않았습니다.")

    decoded_path = "decoded_service_account.json"
    with open(decoded_path, "wb") as f:
        f.write(base64.b64decode(encoded_key))

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(decoded_path, scope)
    return gspread.authorize(creds)
