
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import joblib

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "PXyGqdmIJIoarRn5-PuUEdgRqKZK75cLUHxkbXY6Mlnj"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)

model1 = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = []
    for i in request.form.values():
        int_features.append(float(i))
    # int_features = [float(x) for x in request.form.values()]
    # final_feature = int_features
    print("Test : ",int_features)
    
    payload_scoring = {"input_data": [{"fields": [['cylinders', 'horsepower', 'weight', 'displacement']], "values": [int_features]}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/d14a39a0-173f-43a3-bb37-086e5949e3ba/predictions?version=2022-11-04', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions = response_scoring.json()
    print(predictions)
    predict = predictions['predictions'][0]['values'][0][0]
    predict = round(predict,7)
    print(response_scoring.json())

    #print(final_feature)

    #output = round(prediction[0], 2)
    
    return render_template('index.html', prediction_text='Mileage is {}'.format(predict))


if __name__ == "__main__":
    app.run(debug=True)

@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
'''
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)
