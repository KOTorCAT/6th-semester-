import pandas as pd
import json
import os

def load_lab03_results():
    path = '../03-overfitting-validation-and-hyperparameter-tuning/outputs/baseline_vs_tuned_test_results.csv'
    if os.path.exists(path):
        df = pd.read_csv(path)
        # Выбираем лучшую модель по F1 для каждого датасета
        best = df.loc[df.groupby('dataset')['f1'].idxmax()]
        return best[['dataset','model','feature_set']].to_dict('records')
    return [
        {'dataset':'cardiovascular_risk','model':'LogisticRegression','feature_set':'set_A'},
        {'dataset':'credit_risk','model':'LogisticRegression','feature_set':'set_A'}
    ]

def load_feature_sets():
    path = '../01-feature-importance-and-selection/outputs/feature_sets_wrapper_embedded.json'
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {
        'cardiovascular_risk': {'set_A': ['thalach','oldpeak','age']},
        'credit_risk': {'set_A': ['credit_history','debt_to_income','age']}
    }

def expected_cost(y_true, y_pred, cost_fp=1, cost_fn=5):
    fp = ((y_pred == 1) & (y_true == 0)).sum()
    fn = ((y_pred == 0) & (y_true == 1)).sum()
    n = len(y_true)
    return (fp * cost_fp + fn * cost_fn) / n