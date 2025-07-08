# __init__.py : 해당 디렉토리가 패키지의 일부임을 알려주는 역할
from flask import Flask

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models

    # 블루프린트 등록
    from .views import main_views, question_views, answer_views, auth_views

    # 필터 등록
    from .filter import format_datetime

    app.jinja_env.filters["datetime"] = format_datetime

    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)

    return app
