from fastapi import FastAPI
import os
from google.cloud.exceptions import NotFound
import pandas as pd
from google.cloud import storage
from joblib import load

app = FastAPI()


def load_model():
    if not os.path.exists('logistic_regression_model.joblib'):
        storage_client = storage.Client()
        bucket_name = "mybucket-heartdisease-20245"
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob("models/logistic_regression_model.joblib")
        blob.download_to_filename("logistic_regression_model.joblib")
    model = load("logistic_regression_model.joblib")
    return model

model = load_model()

@app.get('/')
def index():
    return {'ok': True}

@app.get('/predict')
def predict(age, sex, chest_pain, resting_bp, cholesterol, fasting_bs, resting_ecg, max_hr,exercise_angina,oldpeak,st_slope):
    values = [int(age), sex, chest_pain, int(resting_bp), int(cholesterol), int(fasting_bs,), 
              resting_ecg, int(max_hr), exercise_angina, float(oldpeak), st_slope]
    
    df = pd.DataFrame([values], columns = ['Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 'FastingBS',
                                           'RestingECG', 'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope'])

    y_pred = model.predict(df)
    print(y_pred)

    return {'prediction': int(y_pred[0])}

