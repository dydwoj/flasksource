from flask import jsonify, request
from flask import Blueprint


bp = Blueprint("bot", __name__, url_prefix="/")


@bp.route("/chat/", methods=["GET", "POST"])
def chat_get():
    if request.method == "POST":
        kakaorequest = request.get_json()
        print("===========================")
        print(kakaorequest)

    return jsonify({"status": "success"})
