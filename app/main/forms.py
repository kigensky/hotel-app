from flask_wtf import FlaskForm
# from validator import (StringField, TextAreaField,SubmitField, SelectField)
from wtforms import StringField, TextAreaField,SubmitField, SelectField
from wtforms.fields.html5 import DateField, IntegerField
from wtforms.validators import Required, DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed
from .. import photos

class RoomForm(FlaskForm):
    classification = SelectField('Room Classification',validators=[DataRequired()])
    details = TextAreaField('More Details', validators=[DataRequired()])
    cost = IntegerField('Cost per Unit', validators=[DataRequired()])
    units = IntegerField('No. of Units', validators=[DataRequired()])
    image = FileField('Upload image',validators=[FileAllowed(photos, 'Image only!'), FileRequired('File was empty!')])  
    submit = SubmitField('Add Room')

class BookingForm(FlaskForm):
    units = IntegerField('No. of Units', validators=[DataRequired()])
    from_date = DateField('Start Date',  validators=[DataRequired()])
    to_date = DateField('End Date',  validators=[DataRequired()])
    submit = SubmitField("Book")

# format='%m/%d/%Y',
# class CommentForm(FlaskForm):
#     comment = TextAreaField("Post Comment", validators=[Required()])
#     alias = StringField("Comment Alias")
#     submit = SubmitField("Comment")

# class UpdateProfile(FlaskForm):
#     first_name = StringField("First name")
#     last_name = StringField("Last Name")
#     bio = TextAreaField("Bio")
#     email = StringField("Email")
#     submit = SubmitField("Update")
