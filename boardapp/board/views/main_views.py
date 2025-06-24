from flask import Blueprint, redirect, url_for

# Blueprint("별칭", 실행되는 모듈명 가져오기, url_prefix="/")
bp = Blueprint("main", __name__, url_prefix="/")


@bp.route("/")  # == @GetMapping("/")
def index():
    return redirect(url_for("question.list"))
