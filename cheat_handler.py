from flask import jsonify
from gsheet_client import get_gspread_client

client = get_gspread_client()

def handle_cheat_command(text):
    if not text:
        return jsonify({
            "response_type": "ephemeral",
            "text": "❗ 예: `/치트 펫`"
        })

    sheet = client.open_by_key("1wR7HfkOxMP8xeWPNuhTQXGN9cdFFgWTEWrUp_1MBXSQ")
    worksheet = sheet.worksheet("치트키")
    rows = worksheet.get_all_values()

    keyword = text.strip()
    for row in rows[1:]:
        if len(row) >= 3 and keyword in row[1]:
            return jsonify({
                "response_type": "ephemeral",
                "text": f"🎯 `{row[1]}` 치트는 → `{row[2]}` 입니다."
            })

    return jsonify({
        "response_type": "ephemeral",
        "text": "😕 해당 치트키를 찾을 수 없습니다."
    })
