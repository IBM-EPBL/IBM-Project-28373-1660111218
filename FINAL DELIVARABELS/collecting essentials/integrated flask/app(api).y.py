from flask import Flask, render_template, request
import requests
import pickle

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "PHLCdBuZrXUsUSsdNkhkjqBZjB6YF1d_2xkW_ITq6kW7"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)
model = pickle.load(open('university.pkl','rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')
    
@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        GRE= int(request.form['GRE Score'])
        TOEFL=int(request.form['TOEFL Score'])
        select_university_rating=int(request.form['University Rating'])
        SOP=float(request.form['SOP'])
        LOR=float(request.form['LOR'])
        CGPA=float(request.form['CGPA'])
        Research=int(request.form['Research'])

        
        X=[[GRE,TOEFL,select_university_rating,SOP,LOR,CGPA,Research]]
        # NOTE: manually define and pass the array(s) of values to be scored in the next line
        payload_scoring = {"input_data": [{"fields":[[GRE,TOEFL,select_university_rating,SOP,LOR,CGPA,Research]], "values":X}]}

        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/619e085e-542d-4c03-8970-0a48029e159c/predictions?version=2022-11-13', json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")
        prediction=response_scoring.json()
        print(prediction)
        output=prediction['predictions'][0]['values'][0][0]

        if output==True:
            return render_template('index.html',prediction_text="Chance")
        else:
            return render_template('index.html',prediction_text="No Chance")
    else:
        return render_template('index.html')

if __name__=="main":
    app.run(debug=True)