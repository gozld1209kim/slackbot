from flask import jsonify
from gsheet_client import get_gspread_client
import sys  # 디버깅 로그 출력용

client = get_gspread_client()

def handle_monster_command(text):
    if not text:
        return jsonify({
            "response_type": "ephemeral",
            "text": "❗ 예: `/몹검색 슬라임`"
        })

    try:
        sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1bQSv69_gh2_lSaUnTfFTK7VLumf5gPUzfqV3jdCR2VY")
        worksheet = sheet.worksheet("Monster")  # 시트 탭 이름 정확히 확인
        rows = worksheet.get_all_values()
    except Exception as e:
        return jsonify({
            "response_type": "ephemeral",
            "text": f"❌ 시트 접근 실패: {e}"
        })

    keyword = text.strip().casefold()
    matched = []

    # 디버깅: 전체 rows 출력 (Render 로그 확인용)
    print(f"[DEBUG] 검색어: {keyword}", file=sys.stderr)
    print(f"[DEBUG] 총 {len(rows)}행", file=sys.stderr)

    # 데이터 시작 인덱스 파악 (보통 헤더가 2~3줄 있음)
    for i, row in enumerate(rows):
        print(f"[DEBUG] Row {i}: {row}", file=sys.stderr)

    for row in rows[2:]:  # 헤더 2줄 건너뜀
        if len(row) >= 2 and keyword in row[1].strip().casefold():
            matched.append(f"• `{row[1]}` → ID: `{row[0]}`")

    result = "\n".join(matched[:10]) if matched else "😕 검색 결과 없음"
    return jsonify({
        "response_type": "ephemeral",
        "text": f"🔍 `{text}` 검색 결과:\n{result}"
    })
