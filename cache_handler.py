from flask import jsonify
from gsheet_client import _cache
from datetime import datetime

def handle_cache_status():
    """현재 gsheet 캐시 상태를 Slack에 출력"""
    if not _cache:
        return jsonify({
            "response_type": "ephemeral",
            "text": "ℹ️ 현재 활성화된 캐시가 없습니다."
        })

    lines = []
    for key, value in _cache.items():
        expire_str = value["expire"].strftime("%Y-%m-%d %H:%M:%S")
        lines.append(f"• `{key}` → 만료: {expire_str}")

    return jsonify({
        "response_type": "ephemeral",
        "text": "*📦 현재 캐시 상태:*\n" + "\n".join(lines)
    })
