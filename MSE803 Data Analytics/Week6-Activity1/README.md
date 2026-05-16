# Week 6 – Activity 1: Iris Dataset — SVM Classification (Linear Kernel)

**Course:** MSE803 Data Analytics | 2511-YCCIA-MSE  
**Dataset:** Fisher's Iris Dataset (`iris.data`) — 150 samples, 4 features, 3 classes

---

## Dataset Overview

| Attribute | Detail |
|---|---|
| Samples | 150 (50 per class) |
| Features | Sepal Length, Sepal Width, Petal Length, Petal Width (all in cm) |
| Classes | Iris-setosa, Iris-versicolor, Iris-virginica |
| Missing Values | None |
| Duplicates Removed | 3 |

---

## Steps

### 1. Data Loading & Cleaning
- Loaded `iris.data` with no header; assigned column names manually
- Confirmed **no missing values**
- Removed **3 duplicate rows** (147 → cleaned, 150 total original)

### 2. Preprocessing
- Labels encoded with `LabelEncoder`
- Features scaled with `StandardScaler` (required for SVM distance-based classification)
- **80/20 stratified train/test split** → 117 train, 30 test

### 3. SVM Model — Linear Kernel
- Model: `SVC(kernel='linear', C=1.0)`
- Trained on scaled training set
- Predicted on held-out test set

---

## Evaluation Metrics (Test Set — 30 samples)

| Metric | Iris-setosa | Iris-versicolor | Iris-virginica | Overall |
|---|---|---|---|---|
| Precision | 1.00 | 1.00 | 1.00 | **1.00** |
| Recall | 1.00 | 1.00 | 1.00 | **1.00** |
| F1-Score | 1.00 | 1.00 | 1.00 | **1.00** |
| Support | 10 | 10 | 10 | 30 |

**Accuracy: 100.00%**

### Confusion Matrix
```
              Predicted
              setosa  versicolor  virginica
Actual setosa    10       0           0
    versicolor    0      10           0
     virginica    0       0          10
```
Zero misclassifications across all 3 classes.

---

## Results Screenshot

![Results](week6_activity1_results.png)

*6-panel visualisation: Sepal scatter · Petal scatter · Pearson heatmap · Petal length boxplot · Confusion matrix · Precision/Recall/F1 bar chart*

---

## Files

| File | Description |
|---|---|
| `iris.data` | Raw dataset (UCI ML Repository) |
| `week6_activity1_iris_svm.py` | Full Python script: load → clean → visualise → SVM → evaluate |
| `week6_activity1_results.png` | 6-panel output visualisation |
| `README.md` | This file |

---

## Key Insight

The SVM with a **linear kernel** achieves **100% accuracy** on this dataset. This is expected — Iris-setosa is perfectly linearly separable from the other two classes, and with proper feature scaling, the linear hyperplane cleanly separates versicolor from virginica as well. The Pearson heatmap confirms strong correlation between petal length and petal width (r = 0.96), which are the most discriminative features.
