from joblib import Parallel, delayed
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
# import SVC classifier
from sklearn.svm import SVC
# import metrics to compute accuracy
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_scor
import os
from flask import Flask, flash, request, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import logging
from flask import Response
from flask import send_file
from flask import Flask
from flask_cors import CORS, cross_origin


uploaded_df= ""
data_filename= ""
X_test=""
UPLOAD_FOLDER = 'D:/uploads'
ALLOWED_EXTENSIONS = {'csv'}
 
app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

@app.route('/upload_data',  methods=("POST", "GET"))
@cross_origin()
def uploadFile():
    if request.method == 'POST':
        # upload file flask
        global data_filename
        uploaded_df = request.files['uploaded-file']
 
        # Extracting uploaded data file name
        data_filename = secure_filename(uploaded_df.filename)
 
        # flask upload file to database (defined uploaded folder in static path)
        uploaded_df.save("./".join([data_filename]))
 
        # Storing uploaded file path in flask session
        session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], data_filename)
 
        return "Success", 200

@app.route('/process_data',  methods=["GET"])
def process_data():
    response_dict = {}
    svm = joblib.load('./svm.pkl')
    X_test = pd.read_csv(data_filename)
#     X_test = uploaded_df
    final_data = X_test.drop(['isAnomaly','Unnamed: 0.1.1','Unnamed: 0.1','Unnamed: 0', 'device.deviceCategory', 'date', 'geoNetwork.country', 'trafficSource.keyword', 'hits', 'reason'], axis=1)
    y_pred = svm.predict(final_data)
    X_test['isAnomaly'] = y_pred
    X_test.to_csv('./fullnfinal.csv')
    test2 = X_test[X_test['isAnomaly'] == 1]
    n = 5
    response_dict['country'] = test2['geoNetwork.country'].value_counts()[:n].index.tolist()
    response_dict['date'] = test2['date'].value_counts()[:n].index.tolist()
    response_dict['maxHit'] = int(test2['totals.hits'].value_counts().idxmax())
    response_dict['maxTime'] = int(test2['totals.timeOnSite'].value_counts().idxmax())
    response_dict['keyword'] = str(test2['trafficSource.keyword'].value_counts().idxmax())
    response_dict['device'] = str(test2['device.deviceCategory'].value_counts().idxmax())
    response_dict['maxPageView'] = int(test2['totals.pageviews'].value_counts().idxmax())
    return jsonify(response_dict), 200

@app.route('/get_data',  methods=["GET"])
def get_data():
    csv_path = './fullnfinal.csv'
    return send_file(csv_path, as_attachment=True)

if __name__ == "__main__":
    cors = CORS(app)
    app.secret_key = os.urandom(24)
    app.run(debug=True,host="0.0.0.0",use_reloader=False)

# flask_cors.CORS(app, expose_headers='Authorization')



