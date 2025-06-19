from flask import Blueprint

# Blueprint("별칭", 실행되는 모듈명 가져오기, url_prefix="/")
bp = Blueprint("main", __name__, url_prefix="/")


@bp.route("/")  # == @GetMapping("/")
def index():
    return "Hello!!!"
