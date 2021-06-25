from flask_wtf import FlaskForm
from wtforms import StringField
from flask_wtf.file import FileField, FileRequired

class UploadForm(FlaskForm):
    name = StringField('Analysis Name')
    data = FileField('Upload', validators=[FileRequired()])