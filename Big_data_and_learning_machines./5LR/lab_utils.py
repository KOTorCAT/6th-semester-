import pandas as pd
import numpy as np
from sklearn.metrics import f1_score, brier_score_loss
from scipy import stats

# Фиксированные пороги
ALPHA = 0.05
PSI_WARN = 0.10
PSI_ALERT = 0.25
RETRAIN_F1_DROP = 0.05
RETRAIN_COST_INCREASE = 0.15

def expected_cost(y_true, y_pred, cost_fp=1, cost_fn=5):
    fp = ((y_pred == 1) & (y_true == 0)).sum()
    fn = ((y_pred == 0) & (y_true == 1)).sum()
    return (fp * cost_fp + fn * cost_fn) / len(y_true)

def calculate_psi(expected, actual, bins=10):
    """Population Stability Index"""
    expected = np.array(expected)
    actual = np.array(actual)
    
    breakpoints = np.percentile(expected, np.linspace(0, 100, bins+1))
    breakpoints[0] = -np.inf
    breakpoints[-1] = np.inf
    
    expected_bins = np.histogram(expected, bins=breakpoints)[0] / len(expected)
    actual_bins = np.histogram(actual, bins=breakpoints)[0] / len(actual)
    
    expected_bins = np.clip(expected_bins, 0.001, None)
    actual_bins = np.clip(actual_bins, 0.001, None)
    
    psi = np.sum((actual_bins - expected_bins) * np.log(actual_bins / expected_bins))
    return psi

def ks_test(ref, cur):
    """Kolmogorov-Smirnov test"""
    stat, p_value = stats.ks_2samp(ref, cur)
    return stat, p_value

def chi2_test(ref, cur):
    """Chi-square test for categorical features"""
    ref_counts = pd.Series(ref).value_counts()
    cur_counts = pd.Series(cur).value_counts()
    
    all_cats = sorted(set(ref_counts.index) | set(cur_counts.index))
    ref_vec = [ref_counts.get(c, 0) for c in all_cats]
    cur_vec = [cur_counts.get(c, 0) for c in all_cats]
    
    if sum(ref_vec) == 0 or sum(cur_vec) == 0:
        return 0, 1.0
    
    stat, p_value = stats.chisquare(cur_vec, f_exp=ref_vec * sum(cur_vec)/sum(ref_vec))
    return stat, p_value