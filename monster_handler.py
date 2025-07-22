from flask import jsonify
from gsheet_client import get_sheet, force_refresh

def handle_monster_command(text):
    force = text.endswith("*")
    if force:
        text = text[:-1].strip()
        rows = force_refresh("1bQSv69_gh2_lSaUnTfFTK7VLumf5gPUzfqV3jdCR2VY", "Monster")
    else:
        rows = get_sheet("1bQSv69_gh2_lSaUnTfFTK7VLumf5gPUzfqV3jdCR2VY", "Monster")

    if not text:
        return jsonify({
            "response_type": "ephemeral",
            "text": "❗ 예: `/몹검색 슬라임`"
        })

    keyword = text.strip()
    matched = []
    for row in rows[1:]:
        if len(row) >= 2 and keyword in row[1]:
            matched.append(f"• `{row[1]}` → ID: `{row[0]}`")

    result = "\n".join(matched[:10]) if matched else "😕 검색 결과 없음"
    return jsonify({
        "response_type": "ephemeral",
        "text": f"🔍 `{text}` 검색 결과:\n{result}"
    })
