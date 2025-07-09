from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class AdCommentForm(FlaskForm):
    name = StringField("제품명", validators=[DataRequired()])
    brand = StringField("브랜드명", validators=[DataRequired()])
    strength = StringField("제품특징", validators=[DataRequired()])
    tone = StringField("톤앤매너", validators=[DataRequired()])
    keyword = StringField("필수포함키워드", validators=[DataRequired()])
    value = StringField("브랜드핵심가치", validators=[DataRequired()])
