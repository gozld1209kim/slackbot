from flask import jsonify
from gsheet_client import get_gspread_client

client = get_gspread_client()

def handle_monster_command(text):
    if not text:
        return jsonify({
            "response_type": "ephemeral",
            "text": "❗ 예: `/몹검색 늑대`"
        })

    # 시트 URL
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1bQSv69_gh2_lSaUnTfFTK7VLumf5gPUzfqV3jdCR2VY")
    worksheet = sheet.worksheet("Monster")

    # 모든 값 로드
    rows = worksheet.get_all_values()

    # 실제 데이터는 5번째 행부터 시작하므로 rows[4:]
    keyword = text.strip().lower()
    matched = []

    for row in rows[4:]:
        if len(row) >= 2 and keyword in row[1].strip().lower():
            matched.append(f"• `{row[1]}` → ID: `{row[0]}`")

    result = "\n".join(matched[:10]) if matched else "😕 검색 결과 없음"
    return jsonify({
        "response_type": "ephemeral",
        "text": f"🔍 `{text}` 검색 결과:\n{result}"
    })
