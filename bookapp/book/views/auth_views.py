from flask import Blueprint, redirect, url_for, render_template
from book.forms import UserForm

# Blueprint("별칭", 실행되는 모듈명 가져오기, url_prefix="/")
bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/signup/", methods=["POST", "GET"])
def signup():
    form = UserForm()
    return render_template("auth/signup.html")
