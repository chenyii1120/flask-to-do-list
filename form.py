from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class CreateMission(FlaskForm):
    content = StringField(render_kw={"placeholder": "新增任務"})
    submit = SubmitField("新增")
