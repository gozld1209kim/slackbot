import os
import json
import base64
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta

# 환경 변수 재시도 로직
def load_service_account():
    for attempt in range(3):
        encoded = os.environ.get("SERVICE_ACCOUNT_BASE64")
        if encoded:
            try:
                decoded_json = base64.b64decode(encoded).decode("utf-8")
                return json.loads(decoded_json)
            except Exception as e:
                print(f"[ERROR] 서비스 계정 디코딩 실패: {e}")
        print(f"[Retry] SERVICE_ACCOUNT_BASE64 환경변수 로드 실패 ({attempt + 1}/3)...")
        time.sleep(2)  # 2초 간격으로 재시도
    raise EnvironmentError("SERVICE_ACCOUNT_BASE64 환경변수를 찾을 수 없습니다.")

# 서비스 계정 로딩 및 gspread 인증
service_account_info = load_service_account()

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

    return force_refresh(sheet_key, worksheet_name)

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

def get_cache_status():
    """슬랙 명령 등에서 캐시 상태 확인용"""
    status = []
    for key, val in _cache.items():
        ttl = val["expire"] - datetime.now()
        status.append((key, f"{ttl.total_seconds():.0f}초 남음"))
    return status
