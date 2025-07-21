from flask import Flask, request, jsonify
import os
import base64
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# 🔐 Google API 인증 처리
def get_gspread_client():
    encoded_key = os.environ.get("SERVICE_ACCOUNT_BASE64")
    if not encoded_key:
        raise Exception("SERVICE_ACCOUNT_BASE64 환경변수가 설정되지 않았습니다.")
    
    # base64 → json 파일로 디코딩
    decoded_json_path = "decoded_service_account.json"
    with open(decoded_json_path, "wb") as f:
        f.write(base64.b64decode(encoded_key))
    
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(decoded_json_path, scope)
    return gspread.authorize(creds)

# 🔍 스프레드시트 열기
client = get_gspread_client()
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1wR7HfkOxMP8xeWPNuhTQXGN9cdFFgWTEWrUp_1MBXSQ")
worksheet = spreadsheet.get_worksheet(0)  # 첫 번째 시트

@app.route("/slack/command", methods=["POST"])
def slash_command():
    user_input = request.form.get("text", "").strip()

    # 1️⃣ /치트만 입력했을 경우
    if not user_input:
        return jsonify({
            "response_type": "ephemeral",
            "text": "🧙 치트키 전체보기 👉 <https://docs.google.com/spreadsheets/d/1wR7HfkOxMP8xeWPNuhTQXGN9cdFFgWTEWrUp_1MBXSQ|[치트키 링크 열기]>"
        })

    # 2️⃣ /치트 [검색어] 입력했을 경우
    keyword = user_input.lower()
    rows = worksheet.get_all_values()

    matched = []
    for row in rows[3:]:  # 4행부터 검색 (0-index 기준)
        if len(row) >= 3:
            kor = row[1].strip()
            eng = row[2].strip()
            if keyword in kor.lower() or keyword in eng.lower():
                matched.append(f"• `{kor}` / `{eng}`")

    if matched:
        result_text = "\n".join(matched[:10])
    else:
        result_text = "😕 검색된 치트키가 없습니다."

    return jsonify({
        "response_type": "ephemeral",
        "text": f"🔎 `{user_input}` 검색 결과:\n{result_text}"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
