from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
from predict import predict
from googletrans import Translator
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    
    predicted_text = None
    translated_text = None
    if request.method == 'POST':
        if 'img1' not in request.files:
            return redirect(request.url)

        file = request.files['img1']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # Save the uploaded image to the "uploads" folder
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Call the predict function with the image file path
            
            predicted_text = predict(filepath)
            print(predicted_text)
            translator = Translator()
            translation = translator.translate(predicted_text, src='en', dest='ta')
            translated_text = translation.text

    return render_template('index.html', predicted_text= predicted_text,translated_text=translated_text)


if __name__== '__main__':
    app.run(debug=True)