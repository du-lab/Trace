from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DecimalField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired

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

class ParametersForm(FlaskForm):
    window_mz = IntegerField('m/z windows', validators=[DataRequired()])
    window_rt = IntegerField('time window', validators=[DataRequired()])
    mz_r = DecimalField('m/z tolerance', validators=[DataRequired()])

    min_len_eic = IntegerField('EIC min length', validators=[DataRequired()])
    window_size = IntegerField('Window size to calculate noise', validators=[DataRequired()])
    min_snr = IntegerField('Min Signal-to-noise ratio', validators=[DataRequired()])
    perc = IntegerField('Percentile within the window size', validators=[DataRequired()])
    max_scale_for_peak = IntegerField('Max CWT scale', validators=[DataRequired()])

    submit = SubmitField('Submit')