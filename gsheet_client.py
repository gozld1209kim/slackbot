import gspread
from oauth2client.service_account import ServiceAccountCredentials
import base64
import json
import os
import time

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

# 시트별 캐시 저장소
_sheet_cache = {}
_cache_ttl = 86400  # 24시간 (단위: 초)

def get_sheet(sheet_key: str, worksheet_name: str):
    cache_key = f"{sheet_key}:{worksheet_name}"
    now = time.time()

    # 캐시가 있고 유효한 경우 → 캐시된 데이터 반환
    if cache_key in _sheet_cache:
        cached = _sheet_cache[cache_key]
        if now - cached["timestamp"] < _cache_ttl:
            return cached["data"]

    # 캐시가 없거나 만료 → 새로 로드
    sh = gc.open_by_key(sheet_key)
    ws = sh.worksheet(worksheet_name)
    data = ws.get_all_values()

    # 캐시에 저장
    _sheet_cache[cache_key] = {
        "timestamp": now,
        "data": data
    }

    return data

# 필요 시 직접 클라이언트를 사용할 수 있도록 export
def get_gspread_client():
    return gc
