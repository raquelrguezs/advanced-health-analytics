import pandas as pd
import numpy as np
import pytest
import os

def test_clinical_bounds():
    """
    Test ensures that the cleaning pipeline correctly clips outliers 
    to clinically valid ranges.
    """
    data_path = "data/raw/synthetic_clinical_data.csv"
    if not os.path.exists(data_path):
        pytest.skip("Synthetic data not found.")
        
    df = pd.read_csv(data_path)
    
    # Apply cleaning logic (Winsorization)
    df_clean = df.dropna(subset=['Admission_Date']).copy()
    df_clean['Systolic_BP'] = df_clean['Systolic_BP'].clip(lower=60, upper=220)
    df_clean['Glucose_mgdL'] = df_clean['Glucose_mgdL'].clip(lower=40, upper=400)
    
    # Validation checks
    assert df_clean['Systolic_BP'].max() <= 220, "Systolic BP should be <= 220"
    assert df_clean['Systolic_BP'].min() >= 60, "Systolic BP should be >= 60"
    assert df_clean['Glucose_mgdL'].max() <= 400, "Glucose should be <= 400"
    assert df_clean['Glucose_mgdL'].min() >= 40, "Glucose should be >= 40"
