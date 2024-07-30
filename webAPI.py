from flask import Flask, request, redirect, abort, jsonify
import os
from datetime import datetime
import uuid
import json

app = Flask(__name__)
app.config['SECRET-KEY'] = 'uhsd78sd'

# Set the upload folder
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Check if the uploaded file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pptx'

@app.route('/', methods=['GET','POST'])
@app.route('/upload', methods=['GET','POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']

    if file and allowed_file(file.filename):
        # Getting the current date and time for the timestamp
        dt = datetime.now()
        ts = datetime.timestamp(dt)
        uid = str(uuid.uuid4())
        filename = file.filename + str(ts) + uid
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        user_data = {'uid': uid}
        return json.dumps(user_data)

@app.route('/status')
def check_status():
    uid = request.args.get('UID')
    files = os.listdir('uploads')

    file_full_name = ''
    for file in files:
        if uid in file:
            file_full_name = file


    status = 'not found'
    if os.path.isfile("output/"+file_full_name+'.json'):
        status = 'done'
    elif os.path.isfile("uploads/"+file_full_name):
        status = 'pending'

    if status == 'not found':
        return abort(404)

    file_name = file_full_name.split('.')[0] + '.pptx'
    timestamp = file_full_name.replace(file_name, '')
    timestamp = timestamp.replace(uid, '')
    explanation = 'None'
    if status == 'done':
        with open("output/"+file_full_name+'.json', 'r', encoding='utf-8') as file:
            explanation = file.read()

    user_data = {'uid': uid, 'status': status, 'filename': file_name, 'timestamp': timestamp, 'explanation': explanation}
    return json.dumps(user_data)


if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create the upload folder if it doesn't exist
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    app.run(debug=True)
