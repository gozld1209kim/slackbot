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

    keyword = text.strip().lower()
    matched = []

    for row in rows[4:]:  # 실제 데이터는 5행부터 시작
        if len(row) >= 2:
            name = row[1].strip().lower()
            if keyword in name:
                matched.append(f"• `{row[1]}` → ID: `{row[0]}`")

    result = "\n".join(matched[:10]) if matched else "😕 검색 결과 없음"
    return jsonify({
        "response_type": "ephemeral",
        "text": f"🔍 `{text}` 검색 결과:\n{result}"
    })