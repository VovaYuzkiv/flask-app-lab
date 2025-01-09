from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField,DateTimeLocalField
from wtforms.validators import Length, DataRequired
from datetime import datetime as dt

CATEGORIES = [("tech","Tech"),("science","Science"),("lifestyle","Lifestyly")]

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(),Length(min=2,)])
    content = TextAreaField("Content", validators=[DataRequired()],render_kw={"rows":5, "cols":35})
    is_active = BooleanField('Active Post')
    publish_date = DateTimeLocalField('Publish Date', format="%Y-%m-%dT%H:%M", default=dt.now())
    category = SelectField("Category",validators=[DataRequired()],choices=CATEGORIES)
    submit = SubmitField("Add Post")