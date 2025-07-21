from flask import Flask, request, jsonify
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# ✅ Google Sheets 인증
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)

# ✅ 시트 열기
sheet_url = "https://docs.google.com/spreadsheets/d/1wR7HfkOxMP8xeWPNuhTQXGN9cdFFgWTEWrUp_1MBXSQ/edit"
sheet = client.open_by_url(sheet_url).sheet1

@app.route("/slack/command", methods=["POST"])
def slash_command():
    query = request.form.get("text", "").strip().lower()  # 입력 예: "펫"

    if not query:
        return jsonify({
            "response_type": "ephemeral",
            "text": "🔎 `/치트 검색어` 형식으로 입력해주세요. 예: `/치트 펫`"
        })

    # ✅ B열 (한글)과 C열 (영문) 전체 가져오기
    b_col = sheet.col_values(2)[3:]  # B열, 4행부터
    c_col = sheet.col_values(3)[3:]  # C열, 4행부터

    results = []
    for i, (kor, eng) in enumerate(zip(b_col, c_col)):
        if query in kor.lower() or query in eng.lower():
            results.append((kor, eng))

    if not results:
        return jsonify({
            "response_type": "ephemeral",
            "text": f"❌ `{query}` 관련 치트를 찾을 수 없습니다."
        })

    # ✅ 결과 메시지 생성
    msg = f"🔍 `{query}` 관련 치트키 결과:\n"
    for kor, eng in results[:5]:  # 최대 5개 표시
        msg += f"- 🇰🇷 `{kor}` / 🇺🇸 `{eng}`\n"

    return jsonify({
        "response_type": "ephemeral",
        "text": msg
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
