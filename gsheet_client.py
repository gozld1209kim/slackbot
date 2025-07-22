import os
import json
import base64
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta

# 환경 변수에서 base64 인코딩된 서비스 계정 정보 가져오기
encoded = os.environ.get("SERVICE_ACCOUNT_BASE64")
if not encoded:
    raise EnvironmentError("SERVICE_ACCOUNT_BASE64 환경변수가 없습니다.")

# base64 → JSON 파싱
decoded_json = base64.b64decode(encoded).decode("utf-8")
service_account_info = json.loads(decoded_json)

# gspread 인증 설정
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
gc = gspread.authorize(credentials)

# 내부 메모리 캐시
_cache = {}

def get_sheet(sheet_key: str, worksheet_name: str):
    """24시간 캐시된 데이터 가져오기"""
    cache_key = f"{sheet_key}:{worksheet_name}"
    cached = _cache.get(cache_key)

    if cached and cached["expire"] > datetime.now():
        return cached["data"]

    sh = gc.open_by_key(sheet_key)
    worksheet = sh.worksheet(worksheet_name)
    data = worksheet.get_all_values()

    _cache[cache_key] = {
        "data": data,
        "expire": datetime.now() + timedelta(hours=24)
    }
    return data

def force_refresh(sheet_key: str, worksheet_name: str):
    print(f"[force_refresh] 갱신 요청: {sheet_key} / {worksheet_name}")
    sh = gc.open_by_key(sheet_key)
    worksheet = sh.worksheet(worksheet_name)
    data = worksheet.get_all_values()
    print(f"[force_refresh] 새로 가져온 행 수: {len(data)}")

    cache_key = f"{sheet_key}:{worksheet_name}"
    _cache[cache_key] = {
        "data": data,
        "expire": datetime.now() + timedelta(hours=24)
    }
    return data

