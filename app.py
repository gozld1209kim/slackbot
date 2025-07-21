import os
from flask import Flask, request, jsonify
from cheat_handler import handle_cheat_command
from monster_handler import handle_monster_command

app = Flask(__name__)

@app.route("/slack/cheat", methods=["POST"])
def slash_cheat():
    text = request.form.get("text", "")
    return handle_cheat_command(text)

@app.route("/slack/monster", methods=["POST"])
def slash_monster():
    text = request.form.get("text", "")
    return handle_monster_command(text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
