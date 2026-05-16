import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import (
    accuracy_score, classification_report,
    confusion_matrix, ConfusionMatrixDisplay
)

# ─────────────────────────────────────────────
# 1. LOAD
# ─────────────────────────────────────────────
COLS = ["sepal_length", "sepal_width", "petal_length", "petal_width", "species"]
df = pd.read_csv("iris.data", header=None, names=COLS)

print("=" * 60)
print("IRIS DATASET — OVERVIEW")
print("=" * 60)
print(df.head(10).to_string())
print(f"\nShape : {df.shape}")
print(f"Classes: {df['species'].unique()}")

# ─────────────────────────────────────────────
# 2. DATA CLEANING / VALIDATION
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("DATA CLEANING")
print("=" * 60)
print("Missing values:\n", df.isnull().sum())
print("\nDuplicate rows:", df.duplicated().sum())

# Remove any duplicates
df = df.drop_duplicates()
print(f"Shape after de-duplication: {df.shape}")

print("\nClass distribution:\n", df["species"].value_counts())
print("\nDescriptive statistics:")
print(df.describe().round(3))

# ─────────────────────────────────────────────
# 3. ENCODE & SPLIT
# ─────────────────────────────────────────────
le = LabelEncoder()
df["label"] = le.fit_transform(df["species"])

X = df[["sepal_length", "sepal_width", "petal_length", "petal_width"]].values
y = df["label"].values

# 80 / 20 stratified split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# Feature scaling (important for SVM)
scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)

print("\n" + "=" * 60)
print(f"Train samples : {len(X_train)} | Test samples: {len(X_test)}")
print("=" * 60)

# ─────────────────────────────────────────────
# 4. SVM — LINEAR KERNEL
# ─────────────────────────────────────────────
svm = SVC(kernel="linear", C=1.0, random_state=42)
svm.fit(X_train_sc, y_train)
y_pred = svm.predict(X_test_sc)

# ─────────────────────────────────────────────
# 5. EVALUATION METRICS
# ─────────────────────────────────────────────
acc = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred,
                                target_names=le.classes_)
cm = confusion_matrix(y_test, y_pred)

print("\n" + "=" * 60)
print("SVM (Linear Kernel) — EVALUATION METRICS (Test Set)")
print("=" * 60)
print(f"Accuracy : {acc:.4f}  ({acc*100:.2f}%)")
print("\nClassification Report:")
print(report)
print("Confusion Matrix:")
print(cm)

# ─────────────────────────────────────────────
# 6. VISUALISATIONS  (2 × 3 grid)
# ─────────────────────────────────────────────
palette = {"Iris-setosa": "#1B4F72", "Iris-versicolor": "#D97706", "Iris-virginica": "#15803D"}

fig = plt.figure(figsize=(18, 11))
fig.suptitle(
    "Week 6 Activity 1 — Iris Dataset: SVM (Linear Kernel)\nMSE803 Data Analytics",
    fontsize=15, fontweight="bold", y=0.98
)

# ── Plot 1: Sepal scatter ──────────────────
ax1 = fig.add_subplot(2, 3, 1)
for sp, grp in df.groupby("species"):
    ax1.scatter(grp["sepal_length"], grp["sepal_width"],
                label=sp, color=palette[sp], alpha=0.8, edgecolors="white", s=55)
ax1.set_xlabel("Sepal Length (cm)"); ax1.set_ylabel("Sepal Width (cm)")
ax1.set_title("Sepal: Length vs Width", fontweight="bold")
ax1.legend(fontsize=8); ax1.grid(True, alpha=0.3)

# ── Plot 2: Petal scatter ──────────────────
ax2 = fig.add_subplot(2, 3, 2)
for sp, grp in df.groupby("species"):
    ax2.scatter(grp["petal_length"], grp["petal_width"],
                label=sp, color=palette[sp], alpha=0.8, edgecolors="white", s=55)
ax2.set_xlabel("Petal Length (cm)"); ax2.set_ylabel("Petal Width (cm)")
ax2.set_title("Petal: Length vs Width", fontweight="bold")
ax2.legend(fontsize=8); ax2.grid(True, alpha=0.3)

# ── Plot 3: Pairplot-style correlation heatmap ─
ax3 = fig.add_subplot(2, 3, 3)
corr = df[["sepal_length", "sepal_width", "petal_length", "petal_width"]].corr(method="pearson")
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0,
            linewidths=0.8, ax=ax3, annot_kws={"size": 11, "weight": "bold"})
ax3.set_title("Pearson Correlation Heatmap", fontweight="bold")
ax3.set_xticklabels(["Sepal L", "Sepal W", "Petal L", "Petal W"], rotation=25, fontsize=9)
ax3.set_yticklabels(["Sepal L", "Sepal W", "Petal L", "Petal W"], rotation=0, fontsize=9)

# ── Plot 4: Boxplots ───────────────────────
ax4 = fig.add_subplot(2, 3, 4)
feat_data = [df[df["species"] == sp]["petal_length"].values for sp in le.classes_]
bp = ax4.boxplot(feat_data, patch_artist=True,
                 tick_labels=[s.replace("Iris-", "") for s in le.classes_],
                 medianprops=dict(color="crimson", linewidth=2))
colors_box = ["#1B4F72", "#D97706", "#15803D"]
for patch, col in zip(bp["boxes"], colors_box):
    patch.set_facecolor(col); patch.set_alpha(0.7)
ax4.set_title("Petal Length by Species", fontweight="bold")
ax4.set_ylabel("Petal Length (cm)"); ax4.grid(True, alpha=0.3, axis="y")

# ── Plot 5: Confusion Matrix ───────────────
ax5 = fig.add_subplot(2, 3, 5)
disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                               display_labels=[s.replace("Iris-", "") for s in le.classes_])
disp.plot(ax=ax5, colorbar=False, cmap="Blues")
ax5.set_title("Confusion Matrix (Test Set)", fontweight="bold")

# ── Plot 6: Metrics bar chart ──────────────
ax6 = fig.add_subplot(2, 3, 6)
report_dict = classification_report(y_test, y_pred,
                                     target_names=le.classes_, output_dict=True)
species_short = [s.replace("Iris-", "") for s in le.classes_]
metrics = ["precision", "recall", "f1-score"]
x = np.arange(len(species_short))
width = 0.25
bar_colors = ["#1B4F72", "#D97706", "#15803D"]
for j, (metric, col) in enumerate(zip(metrics, bar_colors)):
    vals = [report_dict[sp][metric] for sp in le.classes_]
    bars = ax6.bar(x + j * width, vals, width, label=metric.capitalize(),
                   color=col, alpha=0.85, edgecolor="white")
ax6.axhline(acc, color="crimson", linestyle="--", linewidth=1.5,
            label=f"Accuracy {acc*100:.1f}%")
ax6.set_xticks(x + width)
ax6.set_xticklabels(species_short)
ax6.set_ylim(0, 1.12); ax6.set_ylabel("Score")
ax6.set_title("Precision / Recall / F1 per Class", fontweight="bold")
ax6.legend(fontsize=8); ax6.grid(True, alpha=0.3, axis="y")

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("week6_activity1_results.png", dpi=150, bbox_inches="tight")
plt.show()
print("\nPlot saved → week6_activity1_results.png")
