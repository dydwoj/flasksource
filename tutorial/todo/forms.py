from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired


# DB 에 새로운 구문을 작성하기 위함
# == DTO 역할을 함
class TodoForm(FlaskForm):
    title = StringField(validators=[DataRequired("제목 필수 입력")])  # text
    description = TextAreaField(validators=[DataRequired("상세 필수 입력")])  # textarea
    completed = BooleanField()
    important = BooleanField()
