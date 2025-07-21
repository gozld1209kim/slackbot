from flask import jsonify
from gsheet_client import get_gspread_client
import logging

client = get_gspread_client()

def handle_monster_command(text):
    if not text:
        return jsonify({
            "response_type": "ephemeral",
            "text": "❗ 예: `/몹검색 늑대`"
        })

    logging.info(f"[몹검색] 입력 텍스트: {text}")

    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1bQSv69_gh2_lSaUnTfFTK7VLumf5gPUzfqV3jdCR2VY")
    worksheet = sheet.worksheet("Monster")
    rows = worksheet.get_all_values()

    logging.info(f"[몹검색] 전체 행 수: {len(rows)}")

    keyword = text.strip().lower()
    matched = []

    for i, row in enumerate(rows[4:], start=5):  # 5번째 줄부터 시작
        index = row[0] if len(row) > 0 else ""
        note_cell = row[1] if len(row) > 1 else ""

        logging.debug(f"[몹검색] {i}행 검사: INDEX={index}, NOTE={note_cell}")

        if note_cell and keyword in note_cell.lower():
            matched.append(f"• `{note_cell}` → ID: `{index}`")

    if matched:
        result = "\n".join(matched[:10])
    else:
        result = "😕 검색 결과 없음"

    logging.info(f"[몹검색] 결과 개수: {len(matched)}")

    return jsonify({
        "response_type": "ephemeral",
        "text": f"🔍 `{text}` 검색 결과:\n{result}"
    })
