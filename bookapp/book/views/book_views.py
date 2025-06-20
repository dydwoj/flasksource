from flask import Blueprint, redirect, url_for, render_template, request
from book.models import Book
from book.forms import BookForm
from book import db
from datetime import datetime

bp = Blueprint("book", __name__, url_prefix="/book")


@bp.route("/create/", methods=["GET", "POST"])
def create():

    form = BookForm()
    if request.method == "POST":
        if form.validate_on_submit():
            book = Book(
                title=form.title.data,
                author=form.author.data,
                price=form.price.data,
                description=form.description.data,
                created=datetime.now(),
            )
            db.session.add(book)
            db.session.commit()
            return redirect(url_for("book.list"))

    return render_template("book/create.html", form=form)


@bp.route("/list/")
def list():
    # 페이지 나누기
    # ?page=2
    page = request.args.get("page", type=int, default=1)

    books = Book.query.order_by(Book.code.desc())
    books = books.paginate(page=page, per_page=10)

    return render_template("book/list.html", books=books)


@bp.route("/detail/<int:code>")
def detail(code):
    book = Book.query.get_or_404(code)
    return render_template("book/detail.html", book=book)


@bp.route("/edit/<int:code>", methods=["GET", "POST"])
def edit(code):
    book = Book.query.get_or_404(code)

    if request.method == "POST":
        form = BookForm()
        if form.validate_on_submit():
            form.populate_obj(book)
            db.session.commit()
            return redirect(url_for("book.detail", code=code))
    else:
        # form 과 book 연결
        form = BookForm(obj=book)

    return render_template("book/edit.html", form=form)


@bp.route("/remove/<int:code>")
def remove(code):
    book = Book.query.get_or_404(code)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("book.list"))
