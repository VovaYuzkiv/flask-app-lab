from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField,DateField
from wtforms.validators import Length, DataRequired

CATEGORIES = [("tech","Tech"),("science","Science"),("lifestyle","Lifestyly")]

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(),Length(min=2,)])
    content = TextAreaField("Content", validators=[DataRequired()],render_kw={"rows":5, "cols":35})
    is_active = BooleanField('Active Post')
    publish_date = StringField('Publish Date',validators=[DataRequired()])
    category = SelectField("Category",validators=[DataRequired()],choices=CATEGORIES)
    submit = SubmitField("Add Post")