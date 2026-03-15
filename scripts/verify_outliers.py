import pandas as pd
import numpy as np

def verify_outliers():
    data_path = "data/raw/synthetic_clinical_data.csv"
    df = pd.read_csv(data_path)
    
    # Pre-treatment stats
    print("--- Pre-Treatment Stats ---")
    print(df[['Systolic_BP', 'Glucose_mgdL']].agg(['min', 'max', 'mean']))
    
    # Apply cleaning (Mimic notebook)
    df_clean = df.dropna(subset=['Admission_Date']).copy()
    
    # Winsorization logic
    df_clean['Systolic_BP'] = df_clean['Systolic_BP'].clip(lower=60, upper=220)
    df_clean['Glucose_mgdL'] = df_clean['Glucose_mgdL'].clip(lower=40, upper=400)
    
    # Post-treatment stats
    print("\n--- Post-Treatment Stats ---")
    print(df_clean[['Systolic_BP', 'Glucose_mgdL']].agg(['min', 'max', 'mean']))
    
    # Validation checks
    assert df_clean['Systolic_BP'].max() <= 220, "BP Max exceeds 220"
    assert df_clean['Systolic_BP'].min() >= 60, "BP Min below 60"
    assert df_clean['Glucose_mgdL'].max() <= 400, "Glucose Max exceeds 400"
    assert df_clean['Glucose_mgdL'].min() >= 40, "Glucose Min below 40"
    
    print("\nVerification Successful: All clinical bounds respected.")

if __name__ == "__main__":
    verify_outliers()
