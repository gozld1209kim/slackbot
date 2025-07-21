from flask import jsonify
from gsheet_client import get_gspread_client

client = get_gspread_client()

def handle_monster_command(text):
    if not text:
        return jsonify({
            "response_type": "ephemeral",
            "text": "❗ 예: `/몹검색 슬라임`"
        })

    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1bQSv69_gh2_lSaUnTfFTK7VLumf5gPUzfqV3jdCR2VY")
    worksheet = sheet.worksheet("Monster")
    rows = worksheet.get_all_values()

    # ✅ 숫자로 시작하는 실제 데이터 행부터 시작
    start_index = 0
    for i, row in enumerate(rows):
        if len(row) >= 1 and row[0].strip().isdigit():
            start_index = i
            break

    keyword = text.strip().lower()
    matched = []
    for row in rows[start_index:]:
        if len(row) >= 2 and keyword in row[1].strip().lower():
            matched.append(f"• `{row[1]}` → ID: `{row[0]}`")

    result = "\n".join(matched[:10]) if matched else "😕 검색 결과 없음"
    return jsonify({
        "response_type": "ephemeral",
        "text": f"🔍 `{text}` 검색 결과:\n{result}"
    })
