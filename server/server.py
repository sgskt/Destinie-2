
import os
from flask import Flask, flash, request, redirect, url_for, send_file, render_template
from werkzeug.utils import secure_filename

import datetime
from time import sleep

UPLOAD_FOLDER = '/var/log/destinie/files'
ALLOWED_EXTENSIONS = {'xlsx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/example.xlsx', methods=['GET'])
def example():
    return send_file('example.xlsx', as_attachment=True)


@app.route('/expert', methods=['GET', 'POST'])
def expert_mode():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            prefix = str(datetime.datetime.now()).replace(':', '-').replace(' ', '--')
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], '%s-%s' % (prefix, filename))
            file.save(file_path)


            result_path = '%s.results.xlsx' % file_path[:-5]
            
            myCmd = 'Rscript ../demo/simulation.R --file %s' % file_path

            os.system(myCmd)
            return send_file(result_path, as_attachment=True)
    return render_template('expert.html')


@app.route('/basic', methods=['GET'])
def basic_mode():
    return render_template('basic.html')


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')
