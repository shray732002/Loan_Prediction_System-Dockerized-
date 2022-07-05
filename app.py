# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from flask import Flask,request,render_template,request
import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LogisticRegression
import scipy.stats as stat
app = Flask(__name__)
with open('loan_prediction.pkl', 'rb') as file:  
    model = pickle.load(file)

@app.route('/',methods=['GET','POST'])
def predict_loan_status():
    if request.method=='POST':
        Loan_ID=request.form['Loan_ID']
        Gender=request.form['Gender']
        Married=request.form['Married']
        Dependents=request.form['Dependents']
        Education=request.form['Education']
        Self_Employed=request.form['Self_Employed']
        ApplicantIncome=int(request.form['ApplicantIncome'])
        CoapplicantIncome=float(request.form['CoapplicantIncome'])
        LoanAmount=float(request.form['LoanAmount'])
        Loan_Amount_Term=float(request.form['Loan_Amount_Term'])
        Credit_History=float(request.form['Credit_History'])
        Property_Area=request.form['Property_Area']
        if Gender=="Male":
            Gender = 1
        else:
            Gender = 0
        if Married == "Yes":
            Married = 1
        else:
            Married = 0
        Dependents = int(Dependents.replace('+',''))
        if Education == "Graduate":
            Education = 1
        else:
            Education = 0
        if Self_Employed =="Yes":
            Self_Employed = 1
        else:
            Self_Employed = 0
        TotalIncome = ApplicantIncome+CoapplicantIncome 
        TotalIncome = np.log(TotalIncome)
        LoanAmount= np.log(LoanAmount)
        if Property_Area == "Rural":
            Property_Area = 0
        elif Property_Area == "Semiurban":
            Property_Area = 1
        else:
            Property_Area = 2
        prediction = model.predict([[Gender,Married,Dependents,Education,Self_Employed,LoanAmount,Loan_Amount_Term,Credit_History,Property_Area,TotalIncome]])
        if prediction == 0:
            prediction = "No"
        else:
            prediction = "Yes"
        return render_template("input.html",predictions=str(prediction))
    return render_template('input.html')

if __name__ == "__main__":
    app.run(debug=True)
