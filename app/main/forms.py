from flask_wtf import FlaskForm
# from validator import (StringField, TextAreaField,SubmitField, SelectField)
from wtforms import StringField, TextAreaField,SubmitField, SelectField,IntegerField
from wtforms.validators import Required, DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed
from .. import photos

class RoomForm(FlaskForm):
    classification = SelectField('Classification',validators=[DataRequired()])
    details = TextAreaField('More Details', validators=[DataRequired()])
    units = IntegerField('No. of Units', validators=[DataRequired()])
    image = FileField('Upload image',validators=[FileAllowed(photos, 'Image only!'), FileRequired('File was empty!')])  
    submit = SubmitField('Add Room')

class UpdatePostForm(FlaskForm):
    title = StringField("Blog title", validators=[Required()])
    post = TextAreaField("Type Away", validators=[Required()])
    submit = SubmitField("Update")

class CommentForm(FlaskForm):
    comment = TextAreaField("Post Comment", validators=[Required()])
    alias = StringField("Comment Alias")
    submit = SubmitField("Comment")

class UpdateProfile(FlaskForm):
    first_name = StringField("First name")
    last_name = StringField("Last Name")
    bio = TextAreaField("Bio")
    email = StringField("Email")
    submit = SubmitField("Update")
