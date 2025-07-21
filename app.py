from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/slack/command", methods=["POST"])
def slash_command():
    # 하이퍼링크 적용: <URL|텍스트>
    response_text = "🧙 치트키 바로가기 👉 <https://docs.google.com/spreadsheets/d/1wR7HfkOxMP8xeWPNuhTQXGN9cdFFgWTEWrUp_1MBXSQ/edit?gid=948875907|여기를 클릭하세요>"
    return jsonify({
        "response_type": "in_channel",
        "text": response_text
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
