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
    "IST_ADVANCEMENT_ACCESSORY": "승급 장신구",
    "IST_ADVANCEMENT_ARMOR": "승급 방어구",
    "IST_ADVANCEMENT_PIECE": "승급 조각",
    "IST_ADVANCEMENT_WEAPON": "승급 무기",
    "IST_APPEARANCE_CARD": "외형 카드",
    "IST_ASSIST_CHARGEABLE_TIME_CHARGING": "보조 충전형 시간 충전",
    "IST_BLESS_INTENSION_HIGH_STONE": "축복 강화 상급석",
    "IST_BLESS_INTENSION_SPECIAL_STONE": "축복 강화 특수석",
    "IST_BLESS_INTENSION_STONE": "축복 강화석",
    "IST_BLESS_SUB_COMBINE_HIGH_STONE": "축복 부조합 상급석",
    "IST_BLESS_SUB_COMBINE_SPECIAL_STONE": "축복 부조합 특수석",
    "IST_BLESS_SUB_COMBINE_STONE": "축복 부조합석",
    "IST_BLUNT": "둔기",
    "IST_BODY": "몸통",
    "IST_BOOTS": "부츠",
    "IST_BOW": "활",
    "IST_BOX": "상자",
    "IST_BOX_BOSS": "보스 상자",
    "IST_BOX_CRON": "크론 상자",
    "IST_BOX_EQUIP_CLASS": "클래스 장비 상자",
    "IST_BOX_EQUIP_ENTIRE": "전체 장비 상자",
    "IST_BOX_EQUIP_RANDOM": "랜덤 장비 상자",
    "IST_BOX_EQUIP_SELECT": "선택 장비 상자",
    "IST_BOX_EXP": "경험치 상자",
    "IST_BOX_PAID_CRON": "유료 크론 상자",
    "IST_BOX_PAID_RUBY": "유료 루비 상자",
    "IST_BOX_RANDOM": "랜덤 상자",
    "IST_BOX_RUBY": "루비 상자",
    "IST_BOX_SELECT": "선택 상자",
    "IST_BREAST": "가슴 방어구",
    "IST_CHAR_ADD_SLOT": "캐릭터 슬롯 확장",
    "IST_CLASS": "클래스 관련",
    "IST_CROSSBOW": "석궁",
    "IST_CUSTOMIZING_CHANGE": "커스터마이징 변경",
    "IST_DAGGER": "단검",
    "IST_EARRING": "귀걸이",
    "IST_EMBLEM_ENCHANT": "문장 강화",
    "IST_EMBLEM_UPGRADE": "문장 승급",
    "IST_EMBLEM_UPPER_ENCHANT": "상위 문장 강화",
    "IST_ETC": "기타",
    "IST_FEED": "사료",
    "IST_GACHA_TICKET": "가챠 티켓",
    "IST_GENDER_CHANGE": "성별 변경",
    "IST_GLOVE": "장갑",
    "IST_GUARDER": "수호자",
    "IST_GUILDNAME_CHANGE": "길드명 변경",
    "IST_GUILD_SERVER_MIGRATION": "길드 서버 이전",
    "IST_HEAD": "머리",
    "IST_INTENSION_HIGH_STONE": "강화 상급석",
    "IST_INTENSION_SPECIAL_STONE": "강화 특수석",
    "IST_INTENSION_STONE": "강화석",
    "IST_KATAR": "카타르",
    "IST_KNIGHTSSWORD": "기사검",
    "IST_LANCE": "창",
    "IST_LEG": "하의",
    "IST_NECKLACE": "목걸이",
    "IST_NICKNAME_CHANGE": "닉네임 변경",
    "IST_OPTION_STONE": "옵션석",
    "IST_OPTION_STONE_ETC": "기타 옵션석",
    "IST_ORB": "오브",
    "IST_ORB_GEM": "오브 젬",
    "IST_POTION_HP": "체력 포션",
    "IST_POTION_MP": "마나 포션",
    "IST_PRIVILEGE": "특권",
    "IST_RING": "반지",
    "IST_SCROLL_BUFF": "버프 스크롤",
    "IST_SCROLL_PROP": "속성 스크롤",
    "IST_SCROLL_PROP_GUILD": "길드 속성 스크롤",
    "IST_SCROLL_PROP_PARTY": "파티 속성 스크롤",
    "IST_SCYTHE": "대낫",
    "IST_SERVER_MIGRATION": "서버 이전권",
    "IST_SKILLBOOK_PIECE": "스킬북 조각",
    "IST_SKILL_ACTIVATE": "스킬 활성화",
    "IST_SKILL_ENCHANT": "스킬 강화",
    "IST_SKILL_UPGRADE": "스킬 승급",
    "IST_SPEAR": "창",
    "IST_STAFF": "스태프",
    "IST_STAT_RESET": "능력치 초기화",
    "IST_SUB_COMBINE_HIGH_STONE": "부조합 상급석",
    "IST_SUB_COMBINE_SPECIAL_STONE": "부조합 특수석",
    "IST_SUB_COMBINE_STONE": "부조합석",
    "IST_TRAINING": "훈련",
    "IST_WAND": "완드",
    "IST_ZEN": "젠"
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
