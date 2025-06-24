from flask import Blueprint, redirect, url_for, render_template

# Blueprint("별칭", 실행되는 모듈명 가져오기, url_prefix="/")
bp = Blueprint("question", __name__, url_prefix="/question")


@bp.route("/list/")  # == @GetMapping("/")
def list():
    return render_template("question/list.html")
