import re
import os
import base64
import time
from flask import Blueprint, request, jsonify

predict = Blueprint('predict', __name__)

# Homepage
@predict.route('/predict/')
def handle_predict():
  prediction_probs = ''
  label = ''
  
  if request.method == 'POST':

    data = request.get_json()

    imgstr = re.search(b"base64,(.*)", data['data-uri'].encode()).group(1)
    img_decode = base64.decodebytes(imgstr)
    created_on = time.time()

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], data['amount'])
    filename = os.path.join(filepath, str(created_on) + ".jpg")
    with open(filename, 'wb') as f:
      f.write(img_decode)
  
  return jsonify({'label': label, 'probs': str(prediction_probs)})