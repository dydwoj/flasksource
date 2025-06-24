# application.properties 개념

import os

# config.py 의 경로 가져오기
BASE_DIR = os.path.dirname(__file__)

# 데이터베이스 접속 주소
SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(
    os.path.join(BASE_DIR, "board.db")
)  # 나머진 똑같고 새 프로젝트면 여기서 db 명만 바꿔주기

# 이벤트 처리 옵션
SQLALCHEMY_TRACK_MODIFICATIONS = False

# CSRF 토큰
SECRET_KEY = "dev"
