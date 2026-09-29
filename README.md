# 🌾 AI-Assisted Farmer Disease Diagnostic and Reporting

## Challenge 17 — SIH 1673 | Data Science Hackathon 2026

> Combine crop-image evidence with contextual information to generate a structured disease diagnostic report.

---

### 👥 Team: Solution Squad

| Role | Name |
| :--- | :--- |
| **Team Leader** | Adhesh VS |
| **Member** | Jagadeesh R |
| **Member** | Kishore M |

---

## 📌 Problem Statement

Farmers often detect crop diseases late and expert advice is not always within reach. This project builds an **AI-powered diagnostic engine** that:

1. Accepts a crop leaf image along with contextual metadata (symptoms, weather, crop type).
2. Extracts numerical image features (colour, texture, lesion coverage).
3. Classifies the disease using a **Support Vector Machine (SVM)**.
4. Generates a structured guidance report with confidence scores.

**Prediction Target:** `Crop Disease Class` — 17 classes across 4 crops (Apple, Corn, Potato, Tomato).  
**Specified Algorithm:** SVM (Support Vector Machine).

---

## 📊 Dataset

| Item | Detail |
| :--- | :--- |
| **Source** | [Kaggle — Crop Disease Detection Dataset (PlantVillage)](https://www.kaggle.com/datasets/snikhilrao/crop-disease-detection-dataset) |
| **Crops** | Apple, Corn (Maize), Potato, Tomato |
| **Classes** | 17 disease / healthy classes |
| **Train** | 31,857 images |
| **Validation** | 7,162 images |
| **Test** | 803 images |
| **Feature Dimension** | 2,048 deep features per image |

### Disease Classes

| ID | Class | ID | Class |
| :---: | :--- | :---: | :--- |
| 0 | Apple — Apple Scab | 9 | Potato — Healthy |
| 1 | Apple — Black Rot | 10 | Potato — Late Blight |
| 2 | Apple — Cedar Apple Rust | 11 | Tomato — Bacterial Spot |
| 3 | Apple — Healthy | 12 | Tomato — Early Blight |
| 4 | Corn — Cercospora Leaf Spot | 13 | Tomato — Healthy |
| 5 | Corn — Common Rust | 14 | Tomato — Late Blight |
| 6 | Corn — Healthy | 15 | Tomato — Septoria Leaf Spot |
| 7 | Corn — Northern Leaf Blight | 16 | Tomato — Yellow Leaf Curl Virus |
| 8 | Potato — Early Blight | | |

---

## 🏗️ Repository Structure

```
.
├── README.md                              ← You are here
├── .gitignore
│
├── DS Round 1- solution squad.docx        ← Round 1 presentation document
├── Round_1_Hackathon_Report.docx          ← Formatted report with embedded charts
├── presentation round1.md                 ← Markdown presentation guide
├── DS Data model dashboard.html           ← Interactive HTML dashboard
│
├── farmer_disease_raw_dataset.csv         ← Raw tabular dataset (1,225 records)
├── farmer_disease_cleaned_dataset.csv     ← Cleaned dataset (1,201 records)
├── r_anova_results.csv                    ← R One-Way ANOVA statistical output
│
├── generate_round1_artifacts.py           ← Round 1 — Data prep, EDA & chart generation
├── anova_analysis.R                       ← Round 1 — R ANOVA feature significance testing
├── train_svm_pipeline.py                  ← Round 2 — SVM training & evaluation pipeline
│
├── visualizations/                        ← Python EDA charts (PNG, 300 DPI)
│   ├── chart_1_target_distribution.png
│   ├── chart_2_missing_and_outliers.png
│   ├── chart_3_correlation_heatmap.png
│   ├── chart_4_eda_insights.png
│   └── chart_5_feature_importance.png
│
├── r_visualizations/                      ← R ANOVA charts (PNG)
│   ├── r_anova_f_scores.png
│   ├── r_anova_top_feature_boxplot.png
│   └── r_anova_tukey_hsd.png
│
└── Plant_Disease_Classification/          ← Core ML pipeline
    ├── class_mapping.json
    ├── features/                          ← Extracted deep features (.npz)
    │   ├── train_features.npz
    │   ├── val_features.npz
    │   ├── test_features.npz
    │   ├── class_mapping.json
    │   └── feature_extraction_config.json
    ├── models/                            ← Trained model artifacts
    │   ├── svm_crop_disease_model.joblib
    │   ├── svm_scaler.joblib
    │   └── svm_training_results.json
    ├── eda/                               ← EDA reports, plots & sample images
    │   ├── plots/
    │   ├── reports/
    │   └── samples/
    └── Scripts/                           ← Modular Python pipeline
        ├── 01_dataset_audit.py
        ├── 02_image_quality.py
        ├── 03_duplicate_detection.py
        ├── 04_preprocessing.py
        ├── 05_extract_features.py
        ├── 06_train_svm.py
        ├── 07_evaluate.py
        ├── 08_predict.py
        └── generate_report_graphs.py
```

---

## 🔬 Round 1 — Data Understanding, Preparation & EDA

| Task | Summary |
| :--- | :--- |
| **Objective** | Classify crop disease from leaf images + contextual metadata |
| **Cleaning** | Removed 755 duplicates, fixed 63 inconsistent labels → 17 clean classes, imputed 1,718 missing cells with class-wise median |
| **Outlier Treatment** | IQR Winsorization per class — 3,287 cells capped (no row deletion) |
| **Encoding** | Target: Label Encoding (0–16); Crop: One-Hot; Healthy flag: Binary |
| **Top Features** | `lesion_ratio`, `spot_count`, `mean_H`, `edge_density`, `mean_R` (via ANOVA F-test & Mutual Information) |

### R ANOVA Feature Significance Results

| Feature | F-Statistic | Eta-Squared (η²) | Significance |
| :--- | ---: | ---: | :--- |
| Red_Mean | 1,178.88 | 0.8314 | *** Extremely Significant |
| Leaf_Spot_Coverage_Pct | 1,130.02 | 0.8254 | *** Extremely Significant |
| Green_Mean | 848.08 | 0.7801 | *** Extremely Significant |
| Color_Variance | 563.71 | 0.7023 | *** Extremely Significant |
| Texture_Contrast | 544.14 | 0.6948 | *** Extremely Significant |
| Humidity_Pct | 499.82 | 0.6765 | *** Extremely Significant |

> All 11 tested features achieved p < 0.001 significance for class separability.

---

## 🤖 Round 2 — Feature Engineering & Machine Learning

### SVM Model Performance

| Metric | Score |
| :--- | ---: |
| **Test Accuracy** | **97.51%** |
| **Validation Accuracy** | 97.00% |
| **Macro Precision** | 97.52% |
| **Macro Recall** | 97.44% |
| **Macro F1-Score** | 97.47% |
| **Weighted F1-Score** | 97.51% |
| **Test Error Rate** | 2.49% (20 / 803 samples) |
| **Training Time** | 122.62 seconds |

### Pipeline Steps

1. Load 2,048-dimensional deep features extracted from crop images.
2. Standardize features using `StandardScaler` (fit on train, transform val/test).
3. Train `SGDClassifier(loss='modified_huber')` — Linear SVM with probability outputs.
4. Evaluate with Accuracy, Precision, Recall, F1-score (macro-averaged).
5. Analyse top misclassification pairs for error insights.
6. Save trained model (`svm_crop_disease_model.joblib`) for Round 3 integration.

### Top Misclassification Pairs

| Actual | Predicted | Count |
| :--- | :--- | :---: |
| Corn — Cercospora Leaf Spot | Corn — Northern Leaf Blight | 4 |
| Corn — Northern Leaf Blight | Corn — Cercospora Leaf Spot | 2 |
| Tomato — Early Blight | Tomato — Late Blight | 2 |

> Misclassifications occur between visually similar diseases within the same crop — expected behaviour.

---

## 🚀 Quick Start

### Prerequisites

```bash
pip install numpy pandas scikit-learn matplotlib seaborn opencv-python pillow joblib python-docx xgboost
```

### Run Round 1 — Data Preparation & EDA

```bash
python generate_round1_artifacts.py
Rscript anova_analysis.R
```

### Run Round 2 — SVM Training & Evaluation

```bash
python train_svm_pipeline.py
```

### Run Prediction on New Image

```bash
python Plant_Disease_Classification/Scripts/08_predict.py
```

---

## 📈 Visualizations

### EDA Charts (Round 1)

| Chart | Description |
| :--- | :--- |
| `chart_1_target_distribution.png` | Disease class frequency & percentage distribution |
| `chart_2_missing_and_outliers.png` | Outlier detection & IQR rainfall capping comparison |
| `chart_3_correlation_heatmap.png` | Feature correlation matrix heatmap |
| `chart_4_eda_insights.png` | Leaf spot coverage by class & Red vs Green intensity scatter |
| `chart_5_feature_importance.png` | Mutual Information feature importance ranking |

### R ANOVA Charts

| Chart | Description |
| :--- | :--- |
| `r_anova_f_scores.png` | ANOVA F-statistic ranking bar plot |
| `r_anova_top_feature_boxplot.png` | Top feature distribution boxplot by disease class |
| `r_anova_tukey_hsd.png` | Tukey HSD 95% confidence interval pairwise comparison |

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| Language | Python 3.12, R 4.6 |
| ML Framework | scikit-learn (SVM, SGDClassifier) |
| Feature Extraction | Deep CNN features (2,048-D) |
| Data Processing | pandas, NumPy |
| Visualization | matplotlib, seaborn, R base graphics |
| Statistical Analysis | R ANOVA, Tukey HSD, sklearn ANOVA F-test |
| Dashboard | Power BI / HTML |
| Prototype | Streamlit (Round 3) |

---

## 📝 License

This project was developed for the **Data Science Hackathon 2026** — Challenge 17 (SIH 1673).

---

*Built with ❤️ by Team Solution Squad*
