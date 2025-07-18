from flask import Flask, request, jsonify
import os  # <- 추가해야 합니다

app = Flask(__name__)

@app.route("/slack/command", methods=["POST"])
def slash_command():
    response_text = "🧙 치트키 바로가기 👉 https://your-link.com/cheat"
    return jsonify({
        "response_type": "in_channel",
        "text": response_text
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render가 설정한 포트를 사용
    app.run(host="0.0.0.0", port=port)  # 외부에서 접근 가능하게 설정
