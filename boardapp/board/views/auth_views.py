from flask import (
    Blueprint,
    redirect,
    url_for,
    render_template,
    request,
    session,
    flash,
    g,
)
from werkzeug.security import check_password_hash, generate_password_hash

from board.forms import UserForm, UserLoginForm
from board.models import User
from board import db
import functools

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):

    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next = request.url if request.method == "GET" else ""
            return redirect(url_for("auth.login", next=_next))
        return view(*args, **kwargs)

    return wrapped_view


# 로그인
@bp.route("/login/", methods=["POST", "GET"])
def login():
    form = UserLoginForm()

    if request.method == "POST" and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다"

        if error is None:
            session.clear()
            session["user_id"] = user.id
            # _next 가져오기 (로그인하지 않고 경로를 요청하는 경우 로그인 이후 움직일 경로)
            _next = request.args.get("next", "")
            if _next:
                return redirect(_next)
            else:
                return redirect(url_for("main.index"))
        flash(error)

    return render_template("auth/login.html", form=form)


# 로그인시 사용할 화면
@bp.before_app_request
def load_logged_in_user():
    # 세션에서 정보 가져오기
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


# 로그아웃
@bp.route("/logout/", methods=["POST", "GET"])
def logout():
    session.clear()
    return redirect(url_for("main.index"))


# 회원가입
@bp.route("/signup/", methods=["POST", "GET"])
def signup():
    form = UserForm()

    if request.method == "POST" and form.validate_on_submit():
        # 동일한 id 확인
        user = User.query.filter_by(username=form.username.data).first()
        # 동일하지 않으면 (없으면) 새로운 유저 생성
        if not user:
            user = User(
                username=form.username.data,
                password=generate_password_hash(form.password1.data),
                email=form.email.data,
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("main.index"))
        else:
            flash("이미 존재하는 사용자 입니다")  # 오류 발생

    return render_template("auth/signup.html", form=form)
