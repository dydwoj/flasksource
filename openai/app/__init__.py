# __init__.py : 해당 디렉토리가 패키지의 일부임을 알려주는 역할
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config["WTF_CSRF_ENABLED"] = False

    # 블루프린트 등록
    from . import main_views

    app.register_blueprint(main_views.bp)

    return app
