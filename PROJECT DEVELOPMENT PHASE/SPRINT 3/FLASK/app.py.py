from flask import Flask, render_template, request
import requests
import pickle

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

        
        prediction=model.predict([[GRE,TOEFL,select_university_rating,SOP,LOR,CGPA,Research]])
        output=prediction
        if output==True:
            return render_template('index.html',prediction_text="Chance")
        else:
            return render_template('index.html',prediction_text="No Chance")
    else:
        return render_template('index.html')

if __name__=="main":
    app.run(debug=True)