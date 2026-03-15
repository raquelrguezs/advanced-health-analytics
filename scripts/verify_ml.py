import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

def verify_ml_pipeline():
    data_path = "data/raw/synthetic_clinical_data.csv"
    df = pd.read_csv(data_path)
    
    # Clean data (Condensed)
    df_clean = df.dropna(subset=['Admission_Date']).copy()
    df_clean['Hemoglobin_gdL'] = df_clean['Hemoglobin_gdL'].fillna(df_clean['Hemoglobin_gdL'].median())
    df_clean['Systolic_BP'] = df_clean['Systolic_BP'].clip(60, 220)
    df_clean['Glucose_mgdL'] = df_clean['Glucose_mgdL'].clip(40, 400)
    
    # Feature Engineering
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
    
    print(f"--- ML Verification ---")
    print(f"ROC-AUC Score: {auc:.4f}")
    
    assert auc > 0.65, f"Model performance (AUC={auc:.2f}) is lower than expected for synthetic data."
    
    # Test Risk Function Logic
    high_risk_patient = np.array([[80, 0, 15, 180, 300, 1, 1]]) # Old, long stay, diabetic, hypertension
    high_risk_scaled = scaler.transform(high_risk_patient)
    high_risk_prob = model.predict_proba(high_risk_scaled)[0, 1]
    
    print(f"High-risk test probability: {high_risk_prob:.2f}")
    assert high_risk_prob > 0.5, "High-risk scenario did not yield high probability"
    
    print("\nVerification Successful: ML Pipeline is functional and predictive.")

if __name__ == "__main__":
    verify_ml_pipeline()
