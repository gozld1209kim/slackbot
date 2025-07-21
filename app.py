from flask import Flask, request, jsonify
from gsheet_client import get_gspread_client

app = Flask(__name__)
client = get_gspread_client()

# 시트 ID 정의
CHEAT_SHEET_ID = "1wR7HfkOxMP8xeWPNuhTQXGN9cdFFgWTEWrUp_1MBXSQ"
MONSTER_SHEET_ID = "1bQSv69_gh2_lSaUnTfFTK7VLumf5gPUzfqV3jdCR2VY"

# /치트 명령 처리
@app.route("/slack/cheat", methods=["POST"])
def handle_cheat_command():
    text = request.form.get("text", "").strip()

    if not text:
        return jsonify({
            "response_type": "ephemeral",
            "text": "❗ 예: `/치트 펫`"
        })

    sheet = client.open_by_key(CHEAT_SHEET_ID)
    worksheet = sheet.worksheet("치트키")
    rows = worksheet.get_all_values()

    keyword = text.lower()
    matched = []
    for row in rows[1:]:  # 헤더 제외
        if len(row) >= 3 and keyword in row[1].lower():
            matched.append(f"• `{row[1]}` → `{row[2]}`")

    result = "\n".join(matched[:10]) if matched else "😕 검색 결과 없음"
    return jsonify({
        "response_type": "ephemeral",
        "text": f"🔍 `{text}` 검색 결과:\n{result}"
    })


# /몹검색 명령 처리
@app.route("/slack/monster", methods=["POST"])
def handle_monster_command():
    text = request.form.get("text", "").strip()

    if not text:
        return jsonify({
            "response_type": "ephemeral",
            "text": "❗ 예: `/몹검색 슬라임`"
        })

    sheet = client.open_by_key(MONSTER_SHEET_ID)
    worksheet = sheet.worksheet("Monster")
    rows = worksheet.get_all_values()

    keyword = text.lower()
    matched = []
    for row in rows[1:]:
        if len(row) >= 2 and keyword in row[1].lower():
            matched.append(f"• `{row[1]}` → ID: `{row[0]}`")

    result = "\n".join(matched[:10]) if matched else "😕 검색 결과 없음"
    return jsonify({
        "response_type": "ephemeral",
        "text": f"🔍 `{text}` 검색 결과:\n{result}"
    })


# 서버 실행
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
