from app import app
from flask import render_template, session, redirect, url_for
from werkzeug.utils import secure_filename
from app.forms import UploadForm, ParametersForm
import os, random, string

from app.trace.MasterConfig import params
from app.trace import mzmlReadRaw as read


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Home")

@app.route('/upload', methods=["GET", "POST"])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        session['analysis name'] = form.name.data
        file1 = form.file1.data
        file2 = form.file2.data
        filename1 = secure_filename(file1.filename)
        filename2 = secure_filename(file2.filename)
        folder_name = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        os.mkdir(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads', folder_name))
        file1.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads', folder_name, filename1))
        file2.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads', folder_name, filename2))
        session['filepath1'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads', folder_name, filename1)
        session['filepath2'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads', folder_name, filename2)
        session['run_init_scan'] = True
        return redirect(url_for('parameters'))
    return render_template('upload.html', title="Upload", form=form)

@app.route('/parameters', methods=["GET", "POST"])
def parameters():
    form = ParametersForm()
    if session['run_init_scan'] == True:
        params.CENTROID_MS_PATH = session['filepath1']
        params.PROFILE_MS_PATH = session['filepath2']
        [scan_num, scan_t, mz_list] = read.init_scan(params.PROFILE_MS_PATH)
        params.mz_min = min(mz_list)
        params.mz_max = max(mz_list)
        params.ms_freq = scan_num/(scan_t[len(scan_t)-1]-scan_t[0])
        session['run_init_scan'] = False
    if form.validate_on_submit():
        params.window_mz = form.window_mz.data
        params.window_rt = form.window_rt.data
        params.mz_r = form.mz_r.data
        params.min_len_eic = form.min_len_eic.data
        params.window_size = form.window_size.data
        params.min_snr = form.min_snr.data
        params.perc = form.perc.data
        params.max_scale_for_peak = form.max_scale_for_peak.data
        return redirect(url_for('index'))
    return render_template('parameters.html', title="Parameters", form=form)