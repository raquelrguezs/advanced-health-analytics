import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_mock_clinical_data(n_records=12000):
    """
    Generates a synthetic clinical dataset for readmission prediction.
    Includes 'dirty' data like missing values and outliers.
    """
    np.random.seed(42)
    
    # Generate Patient IDs (some patients appearing multiple times to simulate readmissions)
    patient_ids = np.random.randint(1000, 5000, size=n_records)
    
    # Generate Ages (Normal distribution around 65)
    ages = np.random.normal(65, 15, size=n_records).clip(18, 100).astype(int)
    
    # Gender
    genders = np.random.choice(['M', 'F'], size=n_records)
    
    # Admission Dates
    start_date = datetime(2023, 1, 1)
    admission_dates = [start_date + timedelta(days=np.random.randint(0, 365), 
                                             hours=np.random.randint(0, 24)) 
                       for _ in range(n_records)]
    
    # Duration of Stay (Days)
    stay_duration = np.random.gamma(shape=3, scale=2, size=n_records).clip(1, 25).astype(int)
    
    # Discharge Dates
    discharge_dates = [adm + timedelta(days=int(stay)) for adm, stay in zip(admission_dates, stay_duration)]
    
    # Vital Signs (with outliers)
    # Blood Pressure (Systolic)
    systolic_bp = np.random.normal(125, 15, size=n_records)
    # Inject outliers (e.g., 250 or 40)
    outlier_indices = np.random.choice(n_records, size=int(0.02 * n_records), replace=False)
    systolic_bp[outlier_indices[:len(outlier_indices)//2]] = 240 + np.random.randint(0, 20)
    systolic_bp[outlier_indices[len(outlier_indices)//2:]] = 40 + np.random.randint(0, 10)
    
    # Glucose Levels
    glucose = np.random.normal(100, 20, size=n_records)
    # Outliers
    glucose_outliers = np.random.choice(n_records, size=int(0.01 * n_records), replace=False)
    glucose[glucose_outliers] = 450 + np.random.randint(0, 100)
    
    # Lab Values (with missing values)
    # Hemoglobin
    hemoglobin = np.random.normal(13, 2, size=n_records)
    missing_hgb = np.random.choice(n_records, size=int(0.05 * n_records), replace=False)
    # Will set to NaN later in DataFrame
    
    # Comorbidities (Diabetes, Hypertension, CKD)
    diabetes = np.random.binomial(1, 0.3, size=n_records)
    hypertension = np.random.binomial(1, 0.45, size=n_records)
    
    # Readmission Target (Binary) - influenced by age, stay duration, and glucose
    readmission_prob = (ages / 120) + (stay_duration / 25) + (glucose / 600) + (diabetes * 0.25)
    readmission_prob = readmission_prob.clip(0, 1)
    readmission = np.random.binomial(1, readmission_prob)
    
    # Create DataFrame
    df = pd.DataFrame({
        'Patient_ID': patient_ids,
        'Age': ages,
        'Gender': genders,
        'Admission_Date': admission_dates,
        'Stay_Duration_Days': stay_duration,
        'Discharge_Date': discharge_dates,
        'Systolic_BP': systolic_bp,
        'Glucose_mgdL': glucose,
        'Hemoglobin_gdL': hemoglobin,
        'Diabetes': diabetes,
        'Hypertension': hypertension,
        'Readmitted_30Days': readmission
    })
    
    # Introduce missing timestamps and values
    # Missing Hemoglobin
    df.loc[missing_hgb, 'Hemoglobin_gdL'] = np.nan
    
    # Missing Admission Dates (1%)
    missing_dates = np.random.choice(n_records, size=int(0.01 * n_records), replace=False)
    df.loc[missing_dates, 'Admission_Date'] = pd.NaT
    
    return df

if __name__ == "__main__":
    output_dir = "data/raw"
    os.makedirs(output_dir, exist_ok=True)
    
    print("Generating synthetic clinical data...")
    df = generate_mock_clinical_data(12000)
    
    output_path = os.path.join(output_dir, "synthetic_clinical_data.csv")
    df.to_csv(output_path, index=False)
    
    print(f"Dataset saved to {output_path}")
    print(f"Total records: {len(df)}")
    print(f"Missing values summary:\n{df.isnull().sum()}")
