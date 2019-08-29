import re
import os
import base64
import time
import sys
import numpy as np
import tensorflow as tf
from flask import Blueprint, request, jsonify
from flask import current_app

upload = Blueprint('upload', __name__)

# load the trained model
model = tf.keras.models.load_model("static/models/vnd_classifier_Minhdh.h5")

labels = {'1000': 0,
          '10000': 1,
          '100000': 2,
          '2000': 3,
          '20000': 4,
          '200000': 5,
          '5000': 6,
          '50000': 7,
          '500000': 8
          }

# Homepage
@upload.route('/upload/', methods=['GET', 'POST'])
def handle_upload():
  probabilites = ''
  label = ''
  
  if request.method == 'POST':

    data = request.get_json()

    # Save image to server
    img_raw = re.search(b"base64,(.*)", data['data-uri'].encode()).group(1)
    img_decode = base64.decodebytes(img_raw)
    created_on = time.time()

    filename = os.path.join(current_app.config['UPLOAD_FOLDER'], str(created_on) + ".jpg")
    with open(filename, 'wb') as f:
      f.write(img_decode)

    predict_img_width = current_app.config['PREDICT_IMAGE_WIDTH']
    predict_img_height = current_app.config['PREDICT_IMAGE_HEIGHT']

    image = tf.image.decode_jpeg(img_decode, channels=3)
    image = tf.image.resize(image, [predict_img_width, predict_img_height])
    image = (255 - image) / 255.0  # normalize to [0,1] range
    image = tf.reshape(image, (1, predict_img_width, predict_img_height, 3))

    probabilites = model.predict(image)
    label = np.argmax(probabilites, axis=1).tolist()
    print('label:' + str(label[0]), file=sys.stdout)
    label = [val for val, key in labels.items() if key == label[0]]

    probs = probabilites[0].tolist()
    for val, key in labels.items():
      probs[key] = [val, probs[key]]

    print(probs, file=sys.stdout)

  return jsonify({'label': label, 'probs': probs})