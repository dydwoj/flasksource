from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class BookForm(FlaskForm):
    code = IntegerField("도서코드")
    title = StringField("도서명", validators=[DataRequired("Title 필수 입력")])
    author = StringField("작가명", validators=[DataRequired("Author 필수 입력")])
    price = StringField("가격", validators=[DataRequired("Price 필수 입력")])
    description = TextAreaField()


class UserForm(FlaskForm):
    username = StringField(
        "아이디",
        validators=[
            DataRequired("아이디 필수 입력"),
            Length(min=3, max=20, message="아이디니 3~20자리 사이여야 합니다"),
        ],
    )
    password1 = PasswordField(
        "비밀번호",
        validators=[
            DataRequired("비밀번호 필수 입력"),
            EqualTo("password2", "비밀번호가 일치하지 않습니다"),
        ],
    )
    password2 = PasswordField(
        "비밀번호 확인", validators=[DataRequired("비밀번호 필수 입력")]
    )
    email = EmailField(
        "이메일",
        validators=[DataRequired("이메일 필수 입력"), Email("이메일 형식 확인")],
    )
