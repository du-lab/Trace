from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import InputRequired

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
    window_mz = IntegerField('m/z window', validators=[InputRequired()])
    window_rt = IntegerField('time window', validators=[InputRequired()])
    mz_r = FloatField('m/z tolerance', validators=[InputRequired()])

    min_len_eic = IntegerField('EIC min length', validators=[InputRequired()])
    window_size = IntegerField('Window size to calculate noise', validators=[InputRequired()])
    min_snr = IntegerField('Min Signal-to-noise ratio', validators=[InputRequired()])
    perc = IntegerField('Percentile within the window size', validators=[InputRequired()])
    max_scale_for_peak = IntegerField('Max CWT scale', validators=[InputRequired()])

    mz_min = FloatField('minimum mz')
    mz_max = FloatField('maximum mz')
    ms_freq = FloatField('ms scanning frequency')

    submit = SubmitField('Process')