from flask_wtf import Form
from flask_security.forms import ConfirmRegisterForm
from wtforms import TextField, TextAreaField
from wtforms.validators import InputRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from models import Tag

def enabled_tags():
    return Tag.query.all()

class PostForm(Form):
    title = TextField(u'Title', validators=[InputRequired()])
    text = TextAreaField(u'Text', validators=[InputRequired()])
    tags = QuerySelectMultipleField(query_factory=enabled_tags, allow_blank=True)
    
class CommentForm(Form):
    text = TextAreaField(u'Comment', validators=[InputRequired()])