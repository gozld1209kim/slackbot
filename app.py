import os
from flask import Flask, request
from cheat_handler import handle_cheat_command  # cheat 핸들러 import
from monster_handler import handle_monster_command  # 다른 핸들러도 함께 사용 가능
from item_handler import handle_item_command # 아이템 검색
from pet_handler import handle_pet_command #펫 등급 검색
from ride_handler import handle_ride_command # 탈 것 등급 검색
from item_detail_handler import handle_item_detail_command

app = Flask(__name__)

@app.route("/slack/cheat", methods=["POST"])
def cheat_command():
    text = request.form.get("text", "").strip()
    return handle_cheat_command(text)

@app.route("/slack/monster", methods=["POST"])
def monster_command():
    text = request.form.get("text", "").strip()
    return handle_monster_command(text)

@app.route("/slack/item", methods=["POST"])
def item_command():
    text = request.form.get("text", "").strip()
    return handle_item_command(text)

@app.route("/slack/pet", methods=["POST"])
def pet_command():
    text = request.form.get("text", "").strip()
    return handle_pet_command(text)

@app.route("/slack/ride", methods=["POST"])
def ride_command():
    text = request.form.get("text", "").strip()
    return handle_ride_command(text)

@app.route("/slack/itemdetail", methods=["POST"])
def item_detail():
    text = request.form.get("text", "")
    return handle_item_detail_command(text)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
