
import base64
import numpy as np
from PIL import Image
from flask import Flask, render_template, request, jsonify
import tensorflow
from tensorflow import keras
from keras.models import load_model
import os

IMG_SHAPE = (224,224)
CLASSES = ["Modern", "Old"]
file_path = os.path.abspath("C:/Users/parth/fine_tuned_house.h5")
model = load_model(file_path)

# define this is a flask app
app = Flask(__name__,template_folder='D:/houseInteriorFlask/templates')

# basic first page
@app.route('/')
def sayhello():
      return render_template('index.html')


@app.route('/predict-interior', methods=['POST'])
def predict():
    f = request.files['img']
    fpath = getfpath(f)
    file = Image.open(f)
    file_shape = np.asarray(file).shape

    #Prediction starts here

    # resize image to (224,224) if needed
    if file.size != IMG_SHAPE:
        file = file.resize(IMG_SHAPE)
        file_shape = np.asarray(file).shape

    # pass the image through the network to obtain our predictions
    preds = model.predict(np.expand_dims(file, axis=0))[0]
    i = np.argmax(preds)
    label = CLASSES[i]
    prob = preds[i]

    pred_output = {
        'img_size': file_shape,
        'label': label,
        'probability': np.round(prob * 100, 2)
    }

    return render_template('index.html',
                           img_shape=file_shape,
                           user_image=fpath,
                           pred_output=pred_output
                           )


def getfpath(img) -> str:
    # Even if img was read before, we put the pointer back to beginning of file
    img.seek(0)

    # convert to bases64
    data = img.read()  # get data from file (BytesIO)
    data = base64.b64encode(data)  # convert to base64 as bytes
    data = data.decode()  # convert bytes to string

    # convert to <img> with embed image
    fpath = "data:image/png;base64,{}".format(data)

    return fpath


if __name__ == "__main__":
    app.run(debug=True)