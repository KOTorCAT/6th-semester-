import pandas as pd
import json
import os

def load_feature_sets():
    path = '../01-feature-importance-and-selection/outputs/feature_sets_wrapper_embedded.json'
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {
        'cardiovascular_risk': {
            'full': ['age','sex','trestbps','chol','thalach','oldpeak'],
            'set_A': ['thalach','oldpeak','age']
        },
        'credit_risk': {
            'full': ['age','income','loan_amount','credit_history','debt_to_income','loan_purpose'],
            'set_A': ['credit_history','debt_to_income','age']
        }
    }