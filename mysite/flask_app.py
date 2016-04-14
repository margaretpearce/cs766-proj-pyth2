from flask import Flask
from flask import render_template, send_file, request, json, session
from mysite import kmeans
from PIL import Image
from io import BytesIO
import os
import uuid

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'World'}	#fake user
    return render_template('index.html', title='Home', user=user)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # file upload code here
    if request.method == 'POST':
        file = request.files['file']
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))

        # Save the filename in session
        session['imgfile_to_segment'] = f_name

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
    # Read image from disk
    # img_path = "/home/mlpearce/mysite/static/baboon.jpg"
    img_path = "/home/mlpearce/mysite/static/uploads/914f4b95-06ef-4982-ae33-97db330c0149.jpg"

    if 'imgfile_to_segment' in session:
        img_path = '/home/mlpearce/mysite/static/uploads/'+session['imgfile_to_segment']

    # Fix the number of clusters
    k = 3

    if img_path is not None:
        # Do k means clustering
        result = kmeans.kmeansclustering(img_path, k)
    else:
        print("NO IMAGE RETURNED FROM PATH")

    # Display the resulting image
    img = Image.fromarray(result)

    byte_io = BytesIO()
    img.save(byte_io, 'PNG')
    byte_io.seek(0)

    return send_file(byte_io, mimetype='image/png')