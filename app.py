import numpy as np
import logging
import sys
import datetime
import db_init as db
import tensorflow as tf
from blueprints import *
from flask import Flask, request, jsonify

app = Flask(__name__)
app.register_blueprint(homepage)
app.register_blueprint(upload)
app.register_blueprint(predict)

if __name__ == '__main__':
  app.run(debug=True)

app.debug = True

# App Settings
app.config['PREDICT_IMAGE_WIDTH'] = 192
app.config['PREDICT_IMAGE_HEIGHT'] = 192
app.config['UPLOAD_FOLDER'] = 'uploads'

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