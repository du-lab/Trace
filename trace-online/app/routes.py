from app import app
from flask import render_template, session, redirect, url_for
from werkzeug.utils import secure_filename
from app.forms import UploadForm
import os

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
        file1.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads', filename1))
        file2.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads', filename2))
        session['filepath1'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads', filename1)
        session['filepath2'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads', filename2)
        return redirect(url_for('index'))
    return render_template('upload.html', title="Upload", form=form)