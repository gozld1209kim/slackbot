from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/slack/command", methods=["POST"])
def slash_command():
    response_text = "🧙 치트키 바로가기 👉 https://your-link.com/cheat"
    return jsonify({
        "response_type": "in_channel",
        "text": response_text
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
