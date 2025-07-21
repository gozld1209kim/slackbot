from flask import jsonify
from gsheet_client import get_gspread_client

client = get_gspread_client()

def handle_monster_command(text):
    if not text:
        return jsonify({
            "response_type": "ephemeral",
            "text": "❗ 예: `/몹검색 슬라임`"
        })

    try:
        sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1bQSv69_gh2_lSaUnTfFTK7VLumf5gPUzfqV3jdCR2VY")
        worksheet = sheet.worksheet("Monster")
        rows = worksheet.get_all_values()

        keyword = text.strip()
        matched = []

        for row in rows[1:]:  # 2번째 줄부터 (헤더 제외)
            if len(row) > 1 and row[1]:
                note = row[1].strip()
                if keyword in note:
                    index = row[0].strip() if len(row) > 0 else "N/A"
                    matched.append(f"• `{note}` → ID: `{index}`")

        result = "\n".join(matched[:10]) if matched else "😕 검색 결과 없음"
        return jsonify({
            "response_type": "ephemeral",
            "text": f"🔍 `{text}` 검색 결과:\n{result}"
        })

    except Exception as e:
        return jsonify({
            "response_type": "ephemeral",
            "text": f"❌ 오류 발생: {str(e)}"
        })
