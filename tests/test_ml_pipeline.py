import pandas as pd
import numpy as np
import pytest
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

def test_ml_pipeline():
    """
    Test to verify that the ML pipeline maintains predictive validity 
    (ROC-AUC > 0.70) on synthetic data.
    """
    data_path = "data/raw/synthetic_clinical_data.csv"
    if not os.path.exists(data_path):
        pytest.skip("Synthetic data not found. Run src/generate_clinical_data.py first.")
        
    df = pd.read_csv(data_path)
    
    # Pre-processing pipeline (Condensed for test)
    df_clean = df.dropna(subset=['Admission_Date']).copy()
    df_clean['Hemoglobin_gdL'] = df_clean['Hemoglobin_gdL'].fillna(df_clean['Hemoglobin_gdL'].median())
    df_clean['Systolic_BP'] = df_clean['Systolic_BP'].clip(60, 220)
    df_clean['Glucose_mgdL'] = df_clean['Glucose_mgdL'].clip(40, 400)
    
    le = LabelEncoder()
    df_clean['Gender_Encoded'] = le.fit_transform(df_clean['Gender'])
    
    features = ['Age', 'Gender_Encoded', 'Stay_Duration_Days', 'Systolic_BP', 'Glucose_mgdL', 'Diabetes', 'Hypertension']
    X = df_clean[features]
    y = df_clean['Readmitted_30Days']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Eval
    probs = model.predict_proba(X_test_scaled)[:, 1]
    auc = roc_auc_score(y_test, probs)
    
    assert auc > 0.70, f"Model performance (AUC={auc:.2f}) dropped below threshold."

import os
