import pandas as pd
import json
import os

def load_upstream_artifacts():
    upstream = '../01-feature-importance-and-selection/outputs'
    
    fs_path = os.path.join(upstream, 'feature_sets_wrapper_embedded.json')
    if os.path.exists(fs_path):
        with open(fs_path) as f:
            feature_sets = json.load(f)
    else:
        feature_sets = {
            'cardiovascular_risk': {'set_A': ['thalach', 'oldpeak', 'age']},
            'credit_risk': {'set_A': ['credit_history', 'debt_to_income', 'age']}
        }
    
    mr_path = os.path.join(upstream, 'model_results.csv')
    model_results = pd.read_csv(mr_path) if os.path.exists(mr_path) else None
    
    return {'feature_sets': feature_sets, 'model_results': model_results}