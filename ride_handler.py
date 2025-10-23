from flask import jsonify
from gsheet_client import get_sheet, force_refresh

SPREADSHEET_KEY = "1bQSv69_gh2_lSaUnTfFTK7VLumf5gPUzfqV3jdCR2VY"
SHEET_NAME = "RideInfo"

GRADE_MAP = {
    "일반": "RG_COMMON",
    "고급": "RG_UNCOMMON",
    "희귀": "RG_RARE",
    "고대": "RG_ANCIENT",
    "전설": "RG_LEGEND",
    "신화": "RG_MYTH",
    "유일": "RG_UNIQUE",
}

def handle_ride_command(text):
    force = text.endswith("*")
    if force:
        text = text[:-1].strip()
        rows = force_refresh(SPREADSHEET_KEY, SHEET_NAME)
    else:
        rows = get_sheet(SPREADSHEET_KEY, SHEET_NAME)

    grade_input = text.strip()
    if not grade_input:
        return jsonify({
            "response_type": "ephemeral",
            "text": "❗ 등급을 입력해주세요. 예: `/탈것 희귀`"
        })

    grade_code = GRADE_MAP.get(grade_input)
    if not grade_code:
        return jsonify({
            "response_type": "ephemeral",
            "text": f"⚠️ 유효하지 않은 등급입니다: `{grade_input}`\n가능한 등급: {', '.join(GRADE_MAP.keys())}"
        })

    results = []
    for row in rows[1:]:  # 헤더 제외
        if len(row) >= 8 and row[7] == grade_code:  # H열 → 인덱스 7
            results.append(f"• `{row[0]}` → `{row[1]}`")

    if results:
        return jsonify({
            "response_type": "ephemeral",
            "text": f"🏇 `{grade_input}` 등급 탈것 목록:\n" + "\n".join(results[:10])
        })
    else:
        return jsonify({
            "response_type": "ephemeral",
            "text": f"😕 `{grade_input}` 등급에 해당하는 탈것이 없습니다."
        })
