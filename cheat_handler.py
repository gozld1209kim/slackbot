from flask import jsonify
from gsheet_client import get_gspread_client

client = get_gspread_client()

def handle_cheat_command(text):
    spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1wR7HfkOxMP8xeWPNuhTQXGN9cdFFgWTEWrUp_1MBXSQ")
    worksheet = spreadsheet.get_worksheet(0)
    rows = worksheet.get_all_values()

    if not text:
        return jsonify({
            "response_type": "ephemeral",
            "text": "🧙 전체보기 👉 <https://docs.google.com/spreadsheets/d/1wR7HfkOxMP8xeWPNuhTQXGN9cdFFgWTEWrUp_1MBXSQ|[치트키 보기]>"
        })

    keyword = text.lower()
    matched = []
    for row in rows[3:]:
        if len(row) >= 3 and (keyword in row[1].lower() or keyword in row[2].lower()):
            matched.append(f"• `{row[1]}` / `{row[2]}`")

    result = "\n".join(matched[:10]) if matched else "😕 검색 결과 없음"
    return jsonify({
        "response_type": "ephemeral",
        "text": f"🔍 `{text}` 검색 결과:\n{result}"
    })
