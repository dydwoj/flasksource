from flask import Blueprint, redirect, url_for, render_template, request, g
from board.models import Question
from board.forms import QuestionForm, AnswerForm
from board import db
from datetime import datetime

# Blueprint("별칭", 실행되는 모듈명 가져오기, url_prefix="/")
bp = Blueprint("question", __name__, url_prefix="/question")


@bp.route("/list/")  # == @GetMapping("/")
def list():

    # 페이지 가져오기
    page = request.args.get("page", type=int, default=1)

    question_list = Question.query.order_by(Question.create_date.desc())
    question_list = question_list.paginate(page=page, per_page=10)

    return render_template("question/list.html", question_list=question_list)


@bp.route("/detail/<int:qid>")  # == @GetMapping("/")
def detail(qid):

    question = Question.query.get_or_404(qid)
    form = AnswerForm()

    return render_template("question/detail.html", question=question, form=form)


@bp.route("/create/", methods=["GET", "POST"])  # == @GetMapping("/")
def create():

    form = QuestionForm()
    if request.method == "POST" and form.validate_on_submit():
        question = Question(
            subject=form.subject.data,
            content=form.content.data,
            user=g.user,
            create_date=datetime.now(),
        )
        db.session.add(question)
        db.session.commit()
        return redirect(url_for("main.index"))

    return render_template("question/form.html", form=form)


@bp.route("/modify/<int:qid>", methods=["GET", "POST"])  # == @GetMapping("/")
def modify(qid):

    question = Question.query.get_or_404(qid)
    if request.method == "POST":
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for("question.detail", qid=qid))
    else:
        form = QuestionForm(obj=question)
    return render_template("question/form.html", form=form)


@bp.route("/remove/<int:qid>", methods=["GET", "POST"])  # == @GetMapping("/")
def remove(qid):

    question = Question.query.get_or_404(qid)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for("question.list"))
