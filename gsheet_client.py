import gspread
from oauth2client.service_account import ServiceAccountCredentials
import base64
import json
import os

# 환경변수에서 base64 문자열 가져오기
encoded = os.environ.get("SERVICE_ACCOUNT_BASE64")
if not encoded:
    raise EnvironmentError("환경변수 SERVICE_ACCOUNT_BASE64가 설정되지 않았습니다.")

# base64 디코딩 및 인증정보 로딩
decoded_json = base64.b64decode(encoded).decode("utf-8")
service_account_info = json.loads(decoded_json)

# 인증 및 클라이언트 생성
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
gc = gspread.authorize(credentials)

def get_sheet(sheet_key: str, worksheet_name: str):
    sh = gc.open_by_key(sheet_key)
    return sh.worksheet(worksheet_name)

def get_gspread_client():
    return gc
