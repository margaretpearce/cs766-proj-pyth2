from flask import Flask
from flask import render_template, send_file
from mysite import kmeans
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'World'}	#fake user
    return render_template('index.html', title='Home', user=user)

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
    img_path = "/home/mlpearce/mysite/static/baboon.jpg"

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