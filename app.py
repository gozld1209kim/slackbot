import os
import logging
from flask import Flask, request
from cheat_handler import handle_cheat_command
from monster_handler import handle_monster_command

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route("/slack/command", methods=["POST"])
def handle_command():
    data = request.form
    command = data.get("command")
    text = data.get("text", "").strip()

    logging.info(f"[슬랙 명령어 수신] command: {command}, text: {text}")

    if command == "/치트":
        return handle_cheat_command(text)
    elif command == "/몹검색":
        return handle_monster_command(text)
    else:
        logging.warning(f"❗ 알 수 없는 명령어: {command}")
        return "알 수 없는 명령어입니다.", 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
