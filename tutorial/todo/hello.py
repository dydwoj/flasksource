from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route("/")  # == @GetMapping("/")
def index():
    return "Hello!!!"


@app.route("/create", methods=["GET", "POST"])
def create():
    # return "Create"
    if request.method == "GET":
        return render_template("create.html")
    else:
        name = request.form["name"]
        print(f"name : {name}")
    return redirect("/")


# 자바의 가변변수(pathvariable 과 같은 개념)
@app.route("/read/<int:post_id>")
def read(post_id):
    return f"Read {post_id}"
