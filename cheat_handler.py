from flask import jsonify
from gsheet_client import get_gspread_client

client = get_gspread_client()

# 스프레드시트 고유 키
SPREADSHEET_KEY = "1wR7HfkOxMP8xeWPNuhTQXGN9cdFFgWTEWrUp_1MBXSQ"
SHEET_NAME = "치트키"
SPREADSHEET_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_KEY}/edit"

def handle_cheat_command(text):
    if not text:  # '/치트'만 입력한 경우
        return jsonify({
            "response_type": "ephemeral",
            "text": f"📄 치트키 전체 보기: <{SPREADSHEET_URL}|스프레드시트 열기>"
        })

    keyword = text.strip()
    sheet = client.open_by_key(SPREADSHEET_KEY)
    worksheet = sheet.worksheet(SHEET_NAME)
    rows = worksheet.get_all_values()

    results = []
    for row in rows[1:]:
        if len(row) >= 3 and keyword in row[1]:
            results.append(f"• `{row[1]}` → `{row[2]}`")

    if results:
        return jsonify({
            "response_type": "ephemeral",
            "text": f"🔍 `{keyword}` 관련 치트:\n" + "\n".join(results[:10])
        })
    else:
        return jsonify({
            "response_type": "ephemeral",
            "text": f"😕 `{keyword}`에 대한 치트를 찾을 수 없습니다."
        })
