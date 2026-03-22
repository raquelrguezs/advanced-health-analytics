import pandas as pd
import numpy as np
from scipy import stats
import pytest
import os

def test_statistical_significance():
    """
    Ensures that generated data reflects expected clinical associations 
    between risk factors (Diabetes, LoS) and readmissions.
    """
    data_path = "data/raw/synthetic_clinical_data.csv"
    if not os.path.exists(data_path):
        pytest.skip("Synthetic data not found.")
        
    df = pd.read_csv(data_path)
    
    # Preprocessing
    df_clean = df.dropna(subset=['Admission_Date']).copy()
    df_clean['Hemoglobin_gdL'] = df_clean['Hemoglobin_gdL'].fillna(df_clean['Hemoglobin_gdL'].median())
    df_clean['Systolic_BP'] = df_clean['Systolic_BP'].clip(60, 220)
    df_clean['Glucose_mgdL'] = df_clean['Glucose_mgdL'].clip(40, 400)
    
    # 1. Chi-Square: Diabetes vs Readmission
    contingency = pd.crosstab(df_clean['Diabetes'], df_clean['Readmitted_30Days'])
    chi2, p_chi, _, _ = stats.chi2_contingency(contingency)
    assert p_chi < 0.05, f"Diabetes association was not significant (p={p_chi:.4f})"
    
    # 2. T-Test: Stay Duration vs Readmission
    readmitted = df_clean[df_clean['Readmitted_30Days'] == 1]['Stay_Duration_Days']
    not_readmitted = df_clean[df_clean['Readmitted_30Days'] == 0]['Stay_Duration_Days']
    t_stat, p_t = stats.ttest_ind(readmitted, not_readmitted)
    assert p_t < 0.05, f"Stay duration association was not significant (p={p_t:.4f})"
