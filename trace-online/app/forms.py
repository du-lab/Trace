from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed

class UploadForm(FlaskForm):
    name = StringField('Analysis Name')
    file1 = FileField('Raw data in the centroid mode', validators=[
        FileRequired(),
        FileAllowed(['mzml'], 'mzML format only!')
    ])
    file2 = FileField('Raw data in the profile mode', validators=[
        FileRequired(),
        FileAllowed(['mzml'], 'mzML format only!')
    ])
    submit = SubmitField('Submit')