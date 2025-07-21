from flask import jsonify
from gsheet_client import get_sheet

SPREADSHEET_KEY = "1bQSv69_gh2_lSaUnTfFTK7VLumf5gPUzfqV3jdCR2VY"
SHEET_NAME = "PetInfo"

GRADE_MAP = {
    "일반": "PG_COMMON",
    "고급": "PG_UNCOMMON",
    "희귀": "PG_RARE",
    "고대": "PG_ANCIENT",
    "전설": "PG_LEGEND",
    "신화": "PG_MYTH",
}

def handle_pet_command(text):
    rows = get_sheet(SPREADSHEET_KEY, SHEET_NAME)
    grade_input = text.strip()
    if not grade_input:
        return jsonify({
            "response_type": "ephemeral",
            "text": "❗ 등급을 입력해주세요. 예: `/펫 희귀`"
        })

    grade_code = GRADE_MAP.get(grade_input)
    if not grade_code:
        return jsonify({
            "response_type": "ephemeral",
            "text": f"⚠️ 유효하지 않은 등급입니다: `{grade_input}`\n가능한 등급: {', '.join(GRADE_MAP.keys())}"
        })

    results = []
    for row in rows[1:]:
        if len(row) >= 3 and row[2] == grade_code:
            results.append(f"• `{row[0]}` → `{row[1]}`")

    if results:
        return jsonify({
            "response_type": "ephemeral",
            "text": f"🧬 `{grade_input}` 등급 펫 목록:\n" + "\n".join(results[:10])
        })
    else:
        return jsonify({
            "response_type": "ephemeral",
            "text": f"😕 `{grade_input}` 등급에 해당하는 펫이 없습니다."
        })
