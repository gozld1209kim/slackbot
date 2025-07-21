from flask import jsonify
from gsheet_client import get_gspread_client

client = get_gspread_client()

# 스프레드시트 정보
SPREADSHEET_KEY = "1bQSv69_gh2_lSaUnTfFTK7VLumf5gPUzfqV3jdCR2VY"
SHEET_NAME = "Item"

def handle_item_command(text):
    keyword = text.strip()
    if not keyword:
        return jsonify({
            "response_type": "ephemeral",
            "text": "❗ 검색어를 입력해주세요. 예: `/아이템 마법봉`"
        })

    sheet = client.open_by_key(SPREADSHEET_KEY)
    worksheet = sheet.worksheet(SHEET_NAME)
    rows = worksheet.get_all_values()

    results = []
    for row in rows[1:]:  # 헤더 제외
        if len(row) >= 2 and keyword in row[1]:
            results.append(f"• `{row[0]}` → `{row[1]}`")  # A열: ID, B열: 이름

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
