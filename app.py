import os
from flask import Flask, request
from cheat_handler import handle_cheat_command
from monster_handler import handle_monster_command

app = Flask(__name__)

@app.route("/slack/command", methods=["POST"])
def cheat_command():
    return handle_cheat_command(request.form.get("text", "").strip())

@app.route("/slack/monster", methods=["POST"])
def monster_command():
    return handle_monster_command(request.form.get("text", "").strip())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
