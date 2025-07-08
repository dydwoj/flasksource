from flask import Blueprint, redirect, url_for, render_template, request, g
from board.models import Answer, Question
from board.forms import AnswerForm
from board import db
from datetime import datetime

# Blueprint("별칭", 실행되는 모듈명 가져오기, url_prefix="/")
bp = Blueprint("answer", __name__, url_prefix="/")


@bp.route("/create/<int:qid>", methods=["POST"])  # == @GetMapping("/")
def create(qid):

    form = AnswerForm()
    # 답변과 연관된 질문 찾기
    question = Question.query.get_or_404(qid)

    if request.method == "POST" and form.validate_on_submit():
        # 사용자가 작성한 답변 가져오기
        content = request.form["content"]
        anwser = Answer(content=content, create_date=datetime.now(), user=g.user)
        question.answer_set.append(anwser)
        db.session.commit()
        return redirect(url_for("question.detail", qid=qid))

    return render_template("question/detail.html", question=question, form=form)


@bp.route("/modify/<int:aid>", methods=["GET", "POST"])  # == @GetMapping("/")
def modify(aid):

    answer = Answer.query.get_or_404(aid)
    if request.method == "POST":
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for("question.detail", qid=answer.question.id))
    else:
        form = AnswerForm(obj=answer)
    return render_template("question/answer_form.html", form=form)


@bp.route("/remove/<int:aid>", methods=["GET", "POST"])  # == @GetMapping("/")
def remove(aid):

    answer = Answer.query.get_or_404(aid)
    db.session.delete(answer)
    db.session.commit()
    return redirect(url_for("question.detail", qid=answer.question.id))
