from app import app
from flask import render_template, session, redirect, url_for, request, Response
from werkzeug.utils import secure_filename
from werkzeug.datastructures import MultiDict
from app.forms import UploadForm, ParametersForm
import os, random, string, time

from app.trace.MasterConfig import params
from app.trace import mzmlReadRaw as read
from app.trace.TRACE import main

@app.route('/')
@app.route('/index')
def index():
    if session.get('clear_session') == True:
        session.pop('relative_log_path')
        session.pop('clear_session')
        session.clear()
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
        os.mkdir(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads', folder_name))
        file1.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads', folder_name, filename1))
        file2.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads', folder_name, filename2))
        session['filepath1'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads', folder_name, filename1)
        session['filepath2'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads', folder_name, filename2)
        params.LOGGING_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads', folder_name, 'logs.log')
        session['relative_log_path'] = os.path.relpath(params.LOGGING_PATH, start='')
        return redirect(url_for('parameters'))
    return render_template('upload.html', title="Upload", form=form)

@app.route('/parameters', methods=["GET", "POST"])
def parameters():
    if request.method == 'GET':
        params.CENTROID_MS_PATH = session['filepath1']
        params.PROFILE_MS_PATH = session['filepath2']
        params.RESULTS_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'results')
        params.MEAN_STD_IMGS_PATH = '/Users/ericsun/Projects/Trace/trace-cli/Imgs_mean_std.txt' # Comment out
        params.MODEL_PATH = '/Users/ericsun/Projects/Trace/pre-trained_models/model' # Comment out
        [scan_num, scan_t, mz_list] = read.init_scan(params.PROFILE_MS_PATH)
        params.mz_min = min(mz_list)
        params.mz_max = max(mz_list)
        params.ms_freq = round(scan_num/(scan_t[len(scan_t)-1]-scan_t[0]))
        session['mz_min'], session['mz_max'], session['ms_freq'] = params.mz_min, params.mz_max, params.ms_freq
        form = ParametersForm(formdata=MultiDict({'window_mz': params.window_mz, 'window_rt': params.window_rt,
                                                  'mz_r': params.mz_r, 'min_len_eic': params.min_len_eic,
                                                  'window_size': params.window_size, 'min_snr': params.min_snr,
                                                  'perc': params.perc, 'max_scale_for_peak': params.max_scale_for_peak,
                                                  'mz_min': params.mz_min, 'mz_max': params.mz_max, 'ms_freq': params.ms_freq}))
    else:
        form = ParametersForm()
    if form.validate_on_submit():
        params.window_mz, session['window_mz'] = form.window_mz.data, form.window_mz.data
        params.window_rt, session['window_rt'] = form.window_rt.data, form.window_rt.data
        params.mz_r, session['mz_r'] = form.mz_r.data, form.mz_r.data
        params.min_len_eic, session['min_len_eic'] = form.min_len_eic.data, form.min_len_eic.data
        params.window_size, session['window_size'] = form.window_size.data, form.window_size.data
        params.min_snr, session['min_snr'] = form.min_snr.data, form.min_snr.data
        params.perc, session['perc'] = form.perc.data, form.perc.data
        params.max_scale_for_peak, session['max_scale_for_peak'] = form.max_scale_for_peak.data, form.max_scale_for_peak.data
        session['start_trace'] = True
        return redirect(url_for('result'))
    return render_template('parameters.html', title="Parameters", form=form)

@app.route('/logging')
def logging():
    log_path = session.get('relative_log_path')
    if log_path is None:
        return ''

    # TODO Read lines from log_path and send them to Response
    try:
        log_file = open(log_path)
    except FileNotFoundError:
        return ''
    else:
        # log_file_lines = [line for line in log_file if "HTTP" not in line]
        # log_content = ''.join(log_file_lines)
        # log_file.close()
        log_content = log_file.read()
        log_file.close()
    return Response(log_content, mimetype='text/plain')

@app.route('/result')
def result():
    if session.get('start_trace') == True:
        try:
            log_file = open(session.get('relative_log_path'))
        except TypeError:
            return redirect(url_for('upload'))
        except FileNotFoundError:
            # params.Big_RAM = True
            session['start_trace'] = False
            # session.pop('relative_log_path')
            # session.clear()
            peaks = main(params)
            session['clear_session'] = True
        else:
            log_file.close()
    return render_template('result.html', title="Result", peaks=peaks)