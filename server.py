from predict import predict

import os
from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def home():
    return jsonify({"name": "Berhan API"})


@app.route('/api/v1/predict', methods=['POST'])
def api_predict():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return jsonify({"error": True, "msg": "No file part"})
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return jsonify({"error": True, "msg": "No selected file"})

    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)
        savedfile = os.path.join(app.config['UPLOAD_FOLDER'], filename);
        file.save(savedfile)
        return jsonify({"error": False, "data": predict(savedfile)})

    return jsonify({"error": True, "msg": "Unknow error"})


app.run()
