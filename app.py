from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/slack/command", methods=["POST"])
def slash_command():
    response_text = "🧙 [치트키 링크](https://docs.google.com/spreadsheets/d/1wR7HfkOxMP8xeWPNuhTQXGN9cdFFgWTEWrUp_1MBXSQ/edit?gid=948875907)"
    return jsonify({
        "response_type": "ephemeral",  # ← 요거만 바꾸면 됨!
        "text": response_text
    })

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
