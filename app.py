import numpy as np
import base64
import os
import logging
import re
import sys
import time
import datetime
import db_init as db
import tensorflow as tf
from flask import Flask, flash, escape, render_template, request, send_from_directory, redirect, session, url_for, jsonify

app = Flask(__name__)
app.debug = True
app.config['UPLOAD_FOLDER'] = 'uploads'

# load the trained model
model = tf.keras.models.load_model("static/models/my_model_tl_sigmoid_rmsprop_acc9744.h5")

# change these two values to match the image width and height in the trained model
IMAGE_WIDTH = 170
IMAGE_HEIGHT = 170

def parse_image(imgData):
    imgstr = re.search(rb"base64,(.*)", imgData).group(1)
    img_decode = base64.decodebytes(imgstr)
    with open("output.jpg", "wb") as file:
        file.write(img_decode)
    return img_decode

# Homepage
@app.route('/')
def main():
  return render_template('home.html')

# Handle image upload
@app.route('/upload-image/', methods=['GET', 'POST'])
def upload_image():
  """
  This function handle the upload image request from the frond end user interface
  """
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

# Handle predict correction
@app.route('/predict-correction/', methods=['POST'])
def predict_correction():

  results = {}

  try:
    # get data from the UI form ajax submission
    data_upload_file_path = request.form['upload-file-path']
    data_correction_label = request.form['correction-label']

    if data_upload_file_path != '':
      created_on = datetime.datetime.now()

      # create database table first
      db.create_tables()

      # insert into database
      db.insert_row((data_upload_file_path, data_correction_label, created_on), 'predict_correction')
      results['status'] = 'success'
      results['message'] = 'Thank you for your correction!!!'
  except Exception as error:
    results['status'] = 'exception'
    results['message'] = 'ERROR: ' + error

  return jsonify(results)

if __name__ == '__main__':
  app.run()