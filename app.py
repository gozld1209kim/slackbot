import os
import base64
from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ==========================
# 환경변수에서 서비스 계정 키 복원
# ==========================
encoded_key = os.environ.get("SERVICE_ACCOUNT_BASE64")
if not encoded_key:
    raise Exception("SERVICE_ACCOUNT_BASE64 환경변수가 설정되어 있지 않습니다.")

with open("decoded_service_account.json", "wb") as f:
    f.write(base64.b64decode(encoded_key))

# ==========================
# 구글 스프레드시트 연결
# ==========================
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("decoded_service_account.json", scope)
client = gspread.authorize(creds)

# 열고 싶은 스프레드시트와 시트 선택 (여기서는 첫 번째 시트 사용)
sheet_url = "https://docs.google.com/spreadsheets/d/1wR7HfkOxMP8xeWPNuhTQXGN9cdFFgWTEWrUp_1MBXSQ"
spreadsheet = client.open_by_url(sheet_url)
worksheet = spreadsheet.get_worksheet(0)  # 첫 번째 시트 사용

# ==========================
# Flask 앱 생성
# ==========================
app = Flask(__name__)

@app.route("/slack/command", methods=["POST"])
def slash_command():
    user_input = request.form.get("text", "").strip()  # /치트 [검색어]
    if not user_input:
        return jsonify({
            "response_type": "ephemeral",
            "text": "🔍 검색어를 입력해주세요. 예: `/치트 펫`"
        })

    keyword = user_input.lower()

    # 스프레드시트에서 B열(한글), C열(영문) 검색
    rows = worksheet.get_all_values()
    matched = []
    for row in rows[3:]:  # 4번째 줄부터 데이터 시작 (0-index 기준)
        if len(row) >= 3:
            kor, eng = row[1].strip(), row[2].strip()
            if keyword in kor.lower() or keyword in eng.lower():
                matched.append(f"• `{kor}` / `{eng}`")

    if matched:
        result = "\n".join(matched[:10])
    else:
        result = "😕 검색된 치트키가 없습니다."

    return jsonify({
        "response_type": "ephemeral",  # 본인에게만 표시
        "text": f"🔎 `{user_input}` 검색 결과:\n{result}"
    })

# ==========================
# 로컬 실행
# ==========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
