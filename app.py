import numpy as np
import logging
import sys
import datetime
import db_init as db
import tensorflow as tf
from blueprints import homepage, upload
from flask import Flask

app = Flask(__name__)
app.register_blueprint(homepage)
app.register_blueprint(upload)

if __name__ == '__main__':
  app.run(debug=True)

app.debug = True

# load the trained model
model = tf.keras.models.load_model("static/models/my_model_tl_sigmoid_rmsprop_acc9744.h5")

# change these two values to match the image width and height in the trained model
IMAGE_WIDTH = 170
IMAGE_HEIGHT = 170

  
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