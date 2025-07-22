from flask import jsonify
from gsheet_client import get_sheet

SPREADSHEET_KEY = "1bQSv69_gh2_lSaUnTfFTK7VLumf5gPUzfqV3jdCR2VY"
SHEET_NAME = "Item"

CATEGORY_MAP = {
    "IMT_EQUIP": "장비",
    "IMT_EXPAND": "확장",
    "IMT_MATERIAL": "재료",
    "IMT_MISC": "기타",
}

SUBCATEGORY_MAP = {
    "IDT_ACCESSORY": "장신구",
    "IDT_ADVANCEMENT": "승급",
    "IDT_APPEARANCE_COSTUME": "외형/코스튬",
    "IDT_ARMOR": "방어구",
    "IDT_SKILLBOOK_PIECE": "스킬북 조각",
    "IDT_TRANSITION": "이전",
    "IDT_WEAPON": "무기",
    "IDT_SCROLL": "스크롤",
    "IDT_SELECT": "선택",
    "IDT_SKILL": "스킬",
    "IDT_PET": "펫",
    "IDT_POTION": "포션",
    "IDT_RIDE": "탈것",
    "IDT_MONEY": "재화",
    "IDT_OPTION": "옵션",
    "IDT_PACKAGE": "패키지",
    "IDT_GAIN": "획득",
    "IDT_GROW_ITEM": "성장 아이템",
    "IDT_GUARDER": "수호자",
    "IDT_IDOL": "아이돌",
    "IDT_COSTUME": "코스튬",
    "IDT_EMBLEM": "엠블럼",
    "IDT_ETC": "기타",
    "IDT_ASSIST": "보조",
    "IDT_CHANGE": "변환",
    "IDT_CHARACTER": "캐릭터",
}

DETAILCATEGORY_MAP = {
    "IST_REINFORCE": "강화",
    "IST_SOCKET": "소켓",
    "IST_UPGRADE": "승급",
    "IST_CHANGE": "변환",
    "IST_RANDOM_OPTION": "랜덤옵션",
    "IST_RECOVERY": "회복",
    "IST_BUFF": "버프",
    "IST_BOX": "상자",
    "IST_SELECT_BOX": "선택 상자",
    "IST_ETC": "기타",
    "IST_EVENT": "이벤트",
    "IST_PET_EXP": "펫 경험치",
    "IST_MOUNT_EXP": "탈것 경험치",
    "IST_COLLECTION": "수집",
    "IST_CONSUME": "소비",
    "IST_GROW": "성장",
    "IST_COSTUME": "코스튬",
}

GRADE_MAP = {
    "IG_COMMON": "일반",
    "IG_UNCOMMON": "고급",
    "IG_RARE": "희귀",
    "IG_EPIC": "영웅",
    "IG_LEGEND": "전설",
    "IG_MYTH": "신화",
    "IG_UNIQUE": "유니크",
}

def handle_item_detail_command(text):
    keyword = text.strip()
    if not keyword:
        return jsonify({
            "response_type": "ephemeral",
            "text": "❗ 아이템 index 또는 이름을 입력해주세요. 예: `/아이템상세보기 1000012` 또는 `/아이템상세보기 강화석`"
        })

    rows = get_sheet(SPREADSHEET_KEY, SHEET_NAME)
    header = rows[0]
    matched = None

    for row in rows[1:]:
        index = row[0].strip()
        name = row[3].strip()
        if keyword == index or keyword == name:
            matched = row
            break

    if not matched:
        return jsonify({
            "response_type": "ephemeral",
            "text": f"😕 `{keyword}`에 해당하는 아이템을 찾을 수 없습니다."
        })

    index = matched[0].strip()
    name = matched[3].strip()
    category = CATEGORY_MAP.get(matched[5].strip(), matched[5].strip())
    sub_category = SUBCATEGORY_MAP.get(matched[6].strip(), matched[6].strip())
    detail_category = DETAILCATEGORY_MAP.get(matched[7].strip(), matched[7].strip())
    grade = GRADE_MAP.get(matched[8].strip(), matched[8].strip())

    return jsonify({
        "response_type": "ephemeral",
        "text": (
            f"📦 `{index}` 아이템 상세정보:\n"
            f"• 이름: `{name}`\n"
            f"• 대분류: `{category}`\n"
            f"• 중분류: `{sub_category}`\n"
            f"• 소분류: `{detail_category}`\n"
            f"• 등급: `{grade}`"
        )
    })
