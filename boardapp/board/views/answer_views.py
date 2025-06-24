from flask import Blueprint, redirect, url_for, render_template

# Blueprint("별칭", 실행되는 모듈명 가져오기, url_prefix="/")
bp = Blueprint("answer", __name__, url_prefix="/")


@bp.route("/create/<int:qid>")  # == @GetMapping("/")
def create(qid):
    return render_template("question/list.html")
