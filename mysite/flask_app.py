from flask import Flask
from flask import render_template, request, json, session
from mysite import key, intensity, kmeans, watershed, meanshift_cv, grabcut
from PIL import Image
import os
import uuid
import time
import cv2
import numpy as np

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = key.get_key();

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/splash')
def splash():
    return render_template('splash.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # file upload code here
    if request.method == 'POST':
        file = request.files['file']
        image = np.asarray(bytearray(request.files['file'].read()), dtype="uint8")

        # Read to opencv for resizing
        im = cv2.imdecode(image, cv2.IMREAD_COLOR)
        height = im.shape[0]
        width = im.shape[1]

        mult_x = 1
        mult_y = 1

        # Resize so max length of any side is 300
        if width > 300:
            mult_x = 300 / float(width)
        if height > 300:
            mult_y = 300 / float(height)

        # Scale
        if mult_x < mult_y:
            mult_y = mult_x
        elif mult_x > mult_y:
            mult_x = mult_y

        new_height = int(height*mult_y)
        new_width = int(width*mult_x)

        resized = cv2.resize(im, (new_width, new_height))

        # Save as 'original.*' in a unique subdirectory of '/uploads'
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + '/original' + extension
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f_name)
        dir = os.path.dirname(file_path)

        # Create the directory if it doesn't exist
        if not os.path.exists(dir):
            os.makedirs(dir)

        # Save the file in this directory
        # file.save(file_path)
        cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], f_name), resized)

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

@app.route('/runkmeans/<kval>')
def runkmeans(kval):
    img_path = ""
    folder_path = ""

    # Start a timer
    start = time.time()

    # Read original image from session variable
    if 'imgfile_original' in session:
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], session['imgfile_original'])
        folder_path = str(session['imgfile_original']).split('/')[0]

    # Fix the number of clusters
    k = int(kval)

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
        return json.dumps({'filename':filename, 'time':runtime, 'k':k})
    else:
        print "Could not run kmeans: image not saved in session"

@app.route('/runthresholding')
def runthresholding():
    img_path = ""
    folder_path = ""

    # Start a timer
    start = time.time()

    # Read original image from session variable
    if 'imgfile_original' in session:
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], session['imgfile_original'])
        folder_path = str(session['imgfile_original']).split('/')[0]

    if img_path is not None:
        # Do thresholding
        result, thres = intensity.thresholding(img_path)
        img = Image.fromarray(result)
        filename = folder_path + '/thresholding.png'
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Stop the timer
        end = time.time()
        runtime = end - start

        # Return file URL and time taken to do kmeans
        return json.dumps({'filename':filename, 'time':runtime, 'thres': thres})
    else:
        print "Could not run intensity thresholding: image not saved in session"

@app.route('/runmeanshift')
def runmeanshift():
    img_path = ""
    folder_path = ""

    # Start a timer
    start = time.time()

    # Read original image from session variable
    if 'imgfile_original' in session:
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], session['imgfile_original'])
        folder_path = str(session['imgfile_original']).split('/')[0]

    if img_path is not None:
        result = meanshift_cv.meanshift_cv(img_path)
        img = Image.fromarray(result)
        filename = folder_path + '/meanshift.png'
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Stop the timer
        end = time.time()
        runtime = end - start

        # Return file URL and time taken to do kmeans
        return json.dumps({'filename':filename, 'time':runtime})
    else:
        print "Could not run mean shift: image not saved in session"

@app.route('/rungrabcut/<x>/<y>/<width>/<height>/')
def rungrabcut(x, y, width, height):
    img_path = ""
    folder_path = ""

    # Start a timer
    start = time.time()

    r_x = int(x)
    r_y = int(y)
    r_width = int(width)
    r_height = int(height)

    # Read original image from session variable
    if 'imgfile_original' in session:
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], session['imgfile_original'])
        folder_path = str(session['imgfile_original']).split('/')[0]

    if img_path is not None:
        result = grabcut.grab_cut(img_path, r_x, r_y, r_width, r_height)
        img = Image.fromarray(result)
        filename = folder_path + '/graphcut.png'
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Stop the timer
        end = time.time()
        runtime = end - start

        # Return file URL and time taken to do kmeans
        return json.dumps({'filename':filename, 'time':runtime})
    else:
        print "Could not run graph cut: image not saved in session"

@app.route('/runhybrid')
def runhybrid():
    img_path = ""
    folder_path = ""

    # Start a timer
    start = time.time()

    # Read original image from session variable
    if 'imgfile_original' in session:
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], session['imgfile_original'])
        folder_path = str(session['imgfile_original']).split('/')[0]

    if img_path is not None:
        result = watershed.watershed(img_path)
        img = Image.fromarray(result)
        filename = folder_path + '/hybrid.png'
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Stop the timer
        end = time.time()
        runtime = end - start

        # Return file URL and time taken to do kmeans
        return json.dumps({'filename':filename, 'time':runtime})
    else:
        print "Could not run hybrid: image not saved in session"