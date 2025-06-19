from flask import Blueprint, render_template, request, redirect, url_for
from todo.models import Todo
from todo.forms import TodoForm
from datetime import datetime
from todo import db

# Blueprint("별칭", 실행되는 모듈명 가져오기, url_prefix="/")
bp = Blueprint("todo", __name__, url_prefix="/todo")
# url_prefix -> 기본인 http://127.0.0.1:5000 이후에 뭘 붙일건지의 얘기임


@bp.route("/list/")  # == @GetMapping("/")
def list():
    todos = Todo.query.order_by(Todo.id.desc())
    return render_template("todo/todo_list.html", todos=todos)


@bp.route("/undone/list/")  # == @GetMapping("/")
def undone_list():
    todos = Todo.query.filter(Todo.completed == 0).order_by(Todo.id.desc())
    return render_template("todo/todo_list.html", todos=todos)


# 상세조회
@bp.route("/detail/<int:id>")
def detail(id):
    todo = Todo.query.get_or_404(id)
    return render_template("todo/todo_detail.html", todo=todo)


# 수정
@bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    todo = Todo.query.get_or_404(id)

    if request.method == "POST":
        form = TodoForm()
        if form.validate_on_submit():
            form.populate_obj(
                todo
            )  # 원본 todo 와 form 에 담긴 변경된 todo 사항들을 비교
            db.session.commit()
            return redirect(url_for("todo.detail", id=id))
    else:
        form = TodoForm(obj=todo)
    return render_template("todo/todo_edit.html", form=form)


# 등록
@bp.route("/register/", methods=["GET", "POST"])
def register():
    form = TodoForm()
    if request.method == "POST" and form.validate_on_submit():
        todo = Todo(
            title=form.title.data,
            description=form.description.data,
            important=form.important.data,
            created=datetime.now(),
        )
        db.session.add(todo)
        db.session.commit()

        return redirect(url_for("main.index"))  # == todo.list
    return render_template("todo/todo_create.html", form=form)


# 완료 페이지
@bp.route("/done/<int:id>")
def done(id):
    todo = Todo.query.get_or_404(id)
    todo.completed = True
    db.session.commit()
    return redirect(url_for("todo.detail", id=todo.id))


# 미완료 페이지
@bp.route("/undone/<int:id>")
def undone(id):
    todo = Todo.query.get_or_404(id)
    todo.completed = False
    db.session.commit()
    return redirect(url_for("todo.detail", id=todo.id))


# 완료 리스트
@bp.route("/done/list/")  # == @GetMapping("/")
def done_list():
    todos = Todo.query.filter(Todo.completed == 1).order_by(Todo.id.desc())
    return render_template("todo/todo_list.html", todos=todos)
