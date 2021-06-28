from app import app
from flask import render_template
from app.forms import UploadForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Home")

@app.route('/upload', methods=["GET", "POST"])
def upload():
    form = UploadForm()
    return render_template('upload.html', title="Upload", form=form)