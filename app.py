import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   vorname = request.form.get('vorname')
   nachname = request.form.get('nachname')

   if vorname:
       print('Request for hello page received with vorname=%s' % vorname)
       return render_template('hello.html', vorname = vorname, nachname = nachname)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))

@app.route('/selectfile')
def selectfile():
   print('Request for index page received')
   return render_template('selectfile.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload():
   file = request.files['file']
   if file.filename == '':
        print('No selected file')
        return redirect(request.url)
   if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('upload.html', filename=file.filename)
        # return redirect(url_for('download_file', name=filename))
   else:
       print('Request for hello page received with no file -- redirecting')
       return redirect(url_for('index'))

if __name__ == '__main__':
   app.run()