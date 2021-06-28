from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_wtf.file import FileField, FileRequired

class UploadForm(FlaskForm):
    name = StringField('Analysis Name')
    file1 = FileField('Upload', validators=[FileRequired()])
    file2 = FileField('Upload', validators=[FileRequired()])
    submit = SubmitField('Submit')