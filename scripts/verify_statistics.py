import pandas as pd
import numpy as np
from scipy import stats

def verify_statistics():
    data_path = "data/raw/synthetic_clinical_data.csv"
    df = pd.read_csv(data_path)
    
    # Clean data
    df_clean = df.dropna(subset=['Admission_Date']).copy()
    df_clean['Hemoglobin_gdL'] = df_clean['Hemoglobin_gdL'].fillna(df_clean['Hemoglobin_gdL'].median())
    df_clean['Systolic_BP'] = df_clean['Systolic_BP'].clip(60, 220)
    df_clean['Glucose_mgdL'] = df_clean['Glucose_mgdL'].clip(40, 400)
    
    print("--- Statistical Verification ---")
    
    # 1. Chi-Square: Diabetes
    contingency = pd.crosstab(df_clean['Diabetes'], df_clean['Readmitted_30Days'])
    chi2, p_chi, _, _ = stats.chi2_contingency(contingency)
    print(f"Diabetes Chi2 P-value: {p_chi:.4e}")
    
    # 2. T-Test: Stay Duration
    readmitted = df_clean[df_clean['Readmitted_30Days'] == 1]['Stay_Duration_Days']
    not_readmitted = df_clean[df_clean['Readmitted_30Days'] == 0]['Stay_Duration_Days']
    t_stat, p_t = stats.ttest_ind(readmitted, not_readmitted)
    print(f"Stay Duration T-Test P-value: {p_t:.4e}")
    
    # 3. Demographic Summary
    print("\n--- Demographic Summary ---")
    print(f"Mean Age: {df_clean['Age'].mean():.2f}")
    print(f"Gender Split:\n{df_clean['Gender'].value_counts(normalize=True)}")
    
    assert p_chi < 0.05, "Diabetes should be a significant factor based on our data generation logic"
    assert p_t < 0.05, "Stay duration should be a significant factor"
    
    print("\nVerification Successful: Statistical findings are significant and consistent.")

if __name__ == "__main__":
    verify_statistics()
