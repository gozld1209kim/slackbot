from flask import jsonify
from gsheet_client import get_sheet

SPREADSHEET_KEY = "1bQSv69_gh2_lSaUnTfFTK7VLumf5gPUzfqV3jdCR2VY"
SHEET_NAME = "Item"

def handle_item_command(text):
    rows = get_sheet(SPREADSHEET_KEY, SHEET_NAME)
    keyword = text.strip()
    if not keyword:
        return jsonify({
            "response_type": "ephemeral",
            "text": "❗ 검색어를 입력해주세요. 예: `/아이템 마법봉`"
        })

    results = []
    for row in rows[1:]:
        if len(row) >= 2 and keyword in row[1]:
            results.append(f"• `{row[0]}` → `{row[1]}`")

    if results:
        return jsonify({
            "response_type": "ephemeral",
            "text": f"🔍 `{keyword}` 관련 아이템:\n" + "\n".join(results[:10])
        })
    else:
        return jsonify({
            "response_type": "ephemeral",
            "text": f"😕 `{keyword}`에 해당하는 아이템을 찾을 수 없습니다."
        })
