from board import db


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String, nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    user = db.relationship("User", backref=db.backref("question_set"))
    # manytoone / onetomany 같은 양방향을 열어주기 위한 코드
    modify_date = db.Column(db.DateTime(), nullable=True)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(
        db.Integer, db.ForeignKey("question.id", ondelete="CASCADE"), nullable=False
    )
    question = db.relationship("Question", backref=db.backref("answer_set"))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    user = db.relationship(
        "User", backref=db.backref("answer_set")
    )  # 다대일의 관계에선 다 쪽에서 1에 접근 코드만 넣지만 반대로 1쪽에서 다에 접근하는 방식을 위해서 answer_set 사용함
    modify_date = db.Column(db.DateTime(), nullable=True)


# 사용자
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
