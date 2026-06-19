import pandas as pd
import numpy as np
np.random.seed(42)
n = 500

# Данные 1: cardio
cardio = pd.DataFrame({
    'age': np.random.randint(30, 80, n),
    'sex': np.random.randint(0, 2, n),
    'trestbps': np.random.normal(130, 15, n).astype(int),
    'chol': np.random.normal(240, 50, n).astype(int),
    'thalach': np.random.normal(150, 20, n).astype(int),
    'oldpeak': np.random.normal(1, 0.5, n).round(1),
    'target': np.random.randint(0, 2, n)
})
cardio.to_csv('data/cardiovascular_risk.csv', index=False)

# Данные 2: credit
credit = pd.DataFrame({
    'age': np.random.randint(20, 65, n),
    'income': np.random.normal(50000, 20000, n).astype(int),
    'loan_amount': np.random.normal(15000, 5000, n).astype(int),
    'credit_history': np.random.randint(0, 6, n),
    'debt_to_income': np.random.normal(0.3, 0.1, n).round(2),
    'loan_purpose': np.random.choice(['debt', 'home', 'edu', 'biz'], n),
    'default': np.random.randint(0, 2, n)
})
credit.to_csv('data/credit_risk.csv', index=False)

print("Данные созданы!")