from flask import jsonify

def handle_cheat_command(text):
    if not text:
        return jsonify({
            "response_type": "ephemeral",
            "text": "📘 예: `/치트 링크명`"
        })

    url = f"https://playwith-cheat.netlify.app/?q={text}"
    return jsonify({
        "response_type": "in_channel",
        "text": f"🔗 요청하신 링크입니다: {url}"
    })
