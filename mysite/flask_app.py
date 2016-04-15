from flask import Flask
from flask import render_template, request, json, session
from mysite import kmeans, key
from PIL import Image
import os
import uuid
import sys
import time

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = key.get_key();

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # file upload code here
    if request.method == 'POST':
        file = request.files['file']
        extension = os.path.splitext(file.filename)[1]

        # Save as 'original.*' in a unique subdirectory of '/uploads'
        f_name = str(uuid.uuid4()) + '/original' + extension
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f_name)
        dir = os.path.dirname(file_path)

        # Create the directory if it doesn't exist
        if not os.path.exists(dir):
            os.makedirs(dir)

        # Save the file in this directory
        file.save(file_path)

        # Save the filename in session and return the filename
        session['imgfile_original'] = f_name
        return json.dumps({'filename':f_name})

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/examples')
def examples():
    return render_template('examples.html', title='Examples')

@app.route('/kmeansapp')
def kmeansapp():
    return render_template('kmeans.html', title='K Means')

@app.route('/detect')
def detect():
    img_path = ""
    folder_path = ""

    # Start a timer
    start = time.time()

    # Read original image from session variable
    if 'imgfile_original' in session:
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], session['imgfile_original'])
        folder_path = str(session['imgfile_original']).split('/')[0]

    # Fix the number of clusters
    k = 3

    if img_path is not None:
        # Do k means clustering
        result = kmeans.kmeansclustering(img_path, k)
        img = Image.fromarray(result)
        filename = folder_path + '/kmeans.png'
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Stop the timer
        end = time.time()
        runtime = end - start

        # Return file URL and time taken to do kmeans
        return json.dumps({'filename':filename, 'time':runtime})
    else:
        print "Could not run kmeans: image not saved in session"
