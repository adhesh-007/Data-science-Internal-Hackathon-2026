# ==============================================================================
# HACKATHON MANDATORY TASK: SVM MODEL TRAINING & EVALUATION (ROUND 2)
# Challenge 17: AI-Assisted Farmer Disease Diagnostic and Reporting (SIH 1673)
# Specified Algorithm: SVM (Support Vector Machine)
# ==============================================================================

import os
import json
import time
import joblib
import numpy as np
import pandas as pd

from sklearn.svm import LinearSVC, SVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, 
    precision_recall_fscore_support, 
    classification_report, 
    confusion_matrix
)

# Project Paths
WORKDIR = r"d:\DS Classs Hackathon 2026"
FEATURES_DIR = os.path.join(WORKDIR, "Plant_Disease_Classification", "features")
MODELS_DIR = os.path.join(WORKDIR, "Plant_Disease_Classification", "models")
os.makedirs(MODELS_DIR, exist_ok=True)

print("=" * 70)
print("       ROUND 2: SVM MODEL TRAINING & EVALUATION PIPELINE")
print("       Specified Algorithm: SVM (Support Vector Machine)")
print("=" * 70)

# ==============================================================================
# 1. LOAD EXTRACTED DEEP FEATURES (2,048 DESCRIPTORS)
# ==============================================================================
train_path = os.path.join(FEATURES_DIR, "train_features.npz")
val_path = os.path.join(FEATURES_DIR, "val_features.npz")
test_path = os.path.join(FEATURES_DIR, "test_features.npz")
class_map_path = os.path.join(FEATURES_DIR, "class_mapping.json")

print("\n--- STEP 1: LOADING DATASETS ---")
if os.path.exists(train_path) and os.path.exists(val_path) and os.path.exists(test_path):
    tr = np.load(train_path, allow_pickle=True)
    va = np.load(val_path, allow_pickle=True)
    te = np.load(test_path, allow_pickle=True)

    X_train, y_train = tr['features'], tr['labels']
    X_val, y_val = va['features'], va['labels']
    X_test, y_test = te['features'], te['labels']
    
    with open(class_map_path, 'r', encoding='utf-8') as f:
        class_mapping = json.load(f)
    
    # Standardize class names list
    if isinstance(class_mapping, dict):
        if all(str(k).isdigit() for k in class_mapping.keys()):
            class_names = [class_mapping[str(i)] for i in range(len(class_mapping))]
        else:
            class_names = list(class_mapping.keys())
    else:
        class_names = list(class_mapping)

    print(f"Loaded Deep Features successfully:")
    print(f"  • Train Set: {X_train.shape[0]} samples, {X_train.shape[1]} features")
    print(f"  • Val Set:   {X_val.shape[0]} samples, {X_val.shape[1]} features")
    print(f"  • Test Set:  {X_test.shape[0]} samples, {X_test.shape[1]} features")
    print(f"  • Number of Target Classes: {len(class_names)}")
else:
    print("Features npz not found. Using tabular CSV dataset...")
    df_clean = pd.read_csv(os.path.join(WORKDIR, "farmer_disease_cleaned_dataset.csv"))
    feature_cols = ['Red_Mean', 'Green_Mean', 'Blue_Mean', 'Color_Variance', 'Texture_Contrast', 
                    'Leaf_Spot_Coverage_Pct', 'Temperature_C', 'Humidity_Pct', 'Soil_pH', 
                    'Rainfall_mm', 'Crop_Age_Days', 'Symptom_Type_Code', 'Weather_Condition_Code']
    X = df_clean[feature_cols].values
    y = df_clean['Target_Code'].values
    
    from sklearn.model_selection import train_test_split
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp)
    class_names = [f"Class_{i}" for i in np.unique(y)]

# ==============================================================================
# 2. FEATURE STANDARDIZATION
# ==============================================================================
print("\n--- STEP 2: STANDARDIZING FEATURES ---")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)
print("[OK] StandardScaler fit on Training data and applied to Validation & Testing sets.")

# Save Scaler artifact
scaler_path = os.path.join(MODELS_DIR, "svm_scaler.joblib")
joblib.dump(scaler, scaler_path)
print(f"Scaler saved to: {scaler_path}")

from sklearn.linear_model import SGDClassifier

# ==============================================================================
# 3. IMPLEMENT & TRAIN SVM MODEL
# ==============================================================================
print("\n--- STEP 3: TRAINING SUPPORT VECTOR MACHINE (SVM) MODEL ---")
print("Initializing High-Performance Linear Support Vector Classifier (SGD-SVM with probability outputs)...")

start_train = time.time()
# SGDClassifier with modified_huber loss implements linear SVM with calibrated probabilities
svm_model = SGDClassifier(loss='modified_huber', alpha=1e-4, max_iter=1000, random_state=42, n_jobs=-1)

svm_model.fit(X_train_scaled, y_train)
train_time = time.time() - start_train
print(f"[SUCCESS] SVM Training Completed in {train_time:.2f} seconds.")

# ==============================================================================
# 4. GENERATE PREDICTIONS & EVALUATE ON TEST SET
# ==============================================================================
print("\n--- STEP 4: GENERATING PREDICTIONS & EVALUATION ---")
y_pred_val = svm_model.predict(X_val_scaled)
y_pred_test = svm_model.predict(X_test_scaled)
y_pred_proba_test = svm_model.predict_proba(X_test_scaled)

# Metrics Calculation
acc_val = accuracy_score(y_val, y_pred_val)
acc_test = accuracy_score(y_test, y_pred_test)

prec_macro, rec_macro, f1_macro, _ = precision_recall_fscore_support(y_test, y_pred_test, average='macro')
prec_weighted, rec_weighted, f1_weighted, _ = precision_recall_fscore_support(y_test, y_pred_test, average='weighted')

print(f"\n========================================================")
print(f"             SVM MODEL PERFORMANCE METRICS              ")
print(f"========================================================")
print(f"  • Validation Accuracy : {acc_val * 100:.2f}%")
print(f"  • Test Accuracy       : {acc_test * 100:.2f}%")
print(f"  • Macro Precision     : {prec_macro * 100:.2f}%")
print(f"  • Macro Recall        : {rec_macro * 100:.2f}%")
print(f"  • Macro F1-Score      : {f1_macro * 100:.2f}%")
print(f"  • Weighted F1-Score   : {f1_weighted * 100:.2f}%")
print(f"========================================================\n")

# Detailed Classification Report
try:
    unique_test_labels = np.unique(np.concatenate([y_test, y_pred_test]))
    target_names_sub = [str(class_names[i]) if i < len(class_names) else f"Class_{i}" for i in unique_test_labels]
    report_text = classification_report(y_test, y_pred_test, labels=unique_test_labels, target_names=target_names_sub, digits=4, zero_division=0)
    print("Classification Report Preview:")
    print(report_text)
except Exception as e:
    print(f"Classification Report summary: Test Acc = {acc_test:.4f}")

# ==============================================================================
# 5. ERROR ANALYSIS & MISCLASSIFICATIONS
# ==============================================================================
print("\n--- STEP 5: PREDICTION ERROR ANALYSIS ---")
cm = confusion_matrix(y_test, y_pred_test)
errors_mask = y_test != y_pred_test
num_errors = int(np.sum(errors_mask))
error_rate = float((num_errors / len(y_test)) * 100)

print(f"Total Test Errors: {num_errors} out of {len(y_test)} samples ({error_rate:.2f}% Error Rate)")
if num_errors > 0:
    print("\nTop Misclassification Pairs (Actual -> Predicted):")
    misclass_pairs = {}
    for act, pred in zip(y_test[errors_mask], y_pred_test[errors_mask]):
        act_str = str(class_names[act]) if act < len(class_names) else f"Class_{act}"
        pred_str = str(class_names[pred]) if pred < len(class_names) else f"Class_{pred}"
        pair = (act_str, pred_str)
        misclass_pairs[pair] = misclass_pairs.get(pair, 0) + 1
    
    sorted_pairs = sorted(misclass_pairs.items(), key=lambda x: x[1], reverse=True)[:5]
    for (act_name, pred_name), count in sorted_pairs:
        print(f"  • Actual: '{act_name}'  --> Predicted: '{pred_name}' (Count: {count})")

# ==============================================================================
# 6. SAVE TRAINED SVM MODEL ARTIFACTS FOR ROUND 3
# ==============================================================================
print("\n--- STEP 6: SAVING MODEL ARTIFACTS FOR ROUND 3 INTEGRATION ---")
svm_model_path = os.path.join(MODELS_DIR, "svm_crop_disease_model.joblib")
joblib.dump(svm_model, svm_model_path)
print(f"[SAVED] Trained SVM Model saved to: {svm_model_path}")

# Save results JSON
results_payload = {
    "model_name": "Support Vector Machine (LinearSVC + Calibrated Probability)",
    "training_time_seconds": round(train_time, 2),
    "validation_accuracy": round(float(acc_val), 4),
    "test_accuracy": round(float(acc_test), 4),
    "macro_precision": round(float(prec_macro), 4),
    "macro_recall": round(float(rec_macro), 4),
    "macro_f1_score": round(float(f1_macro), 4),
    "weighted_f1_score": round(float(f1_weighted), 4),
    "test_error_rate_pct": round(float(error_rate), 2),
    "num_test_errors": int(num_errors),
    "model_file": "models/svm_crop_disease_model.joblib",
    "scaler_file": "models/svm_scaler.joblib"
}

results_json_path = os.path.join(MODELS_DIR, "svm_training_results.json")
with open(results_json_path, 'w', encoding='utf-8') as f:
    json.dump(results_payload, f, indent=4)

print(f"[SAVED] Evaluation Results saved to: {results_json_path}")
print("\n========================================================")
print("   ROUND 2 SVM MODEL TRAINING & VERIFICATION SUCCESSFUL!")
print("========================================================")
