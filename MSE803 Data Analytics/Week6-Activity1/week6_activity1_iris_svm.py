import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import seaborn as sns
from matplotlib.patches import Ellipse
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
print(f"\nShape  : {df.shape}")
print(f"Classes: {df['species'].unique()}")

# ─────────────────────────────────────────────
# 2. DATA CLEANING
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("DATA CLEANING")
print("=" * 60)
print("Missing values:\n", df.isnull().sum())
dups = df.duplicated().sum()
print(f"\nDuplicate rows: {dups}")
df = df.drop_duplicates()
print(f"Shape after de-duplication: {df.shape}")
print("\nClass distribution:\n", df["species"].value_counts())
print("\nDescriptive statistics:")
print(df.describe().round(3))

# ─────────────────────────────────────────────
# 3. ENCODE, SCALE & SPLIT
# ─────────────────────────────────────────────
le = LabelEncoder()
df["label"] = le.fit_transform(df["species"])

X = df[["sepal_length", "sepal_width", "petal_length", "petal_width"]].values
y = df["label"].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)

print(f"\nTrain: {len(X_train)} samples  |  Test: {len(X_test)} samples")

# ─────────────────────────────────────────────
# 4. SVM — LINEAR KERNEL  (full 4-feature model)
# ─────────────────────────────────────────────
svm = SVC(kernel="linear", C=1.0, random_state=42)
svm.fit(X_train_sc, y_train)
y_pred = svm.predict(X_test_sc)

acc = accuracy_score(y_test, y_pred)
report_dict = classification_report(
    y_test, y_pred, target_names=le.classes_, output_dict=True
)
cm = confusion_matrix(y_test, y_pred)

print("\n" + "=" * 60)
print("SVM (Linear Kernel) — EVALUATION METRICS (Test Set)")
print("=" * 60)
print(f"Accuracy : {acc:.4f}  ({acc*100:.2f}%)")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=le.classes_))
print("Confusion Matrix:")
print(cm)

# ─────────────────────────────────────────────
# 5. 2-D SVM for decision-boundary plot
#    (re-trained on petal features only for visualisation)
# ─────────────────────────────────────────────
svm_2d = SVC(kernel="linear", C=1.0, random_state=42)
X_tr_2d = X_train_sc[:, [2, 3]]   # petal length & width (scaled)
svm_2d.fit(X_tr_2d, y_train)

# ─────────────────────────────────────────────
# 6. CONFIDENCE-ELLIPSE HELPER
# ─────────────────────────────────────────────
def confidence_ellipse(x, y, ax, n_std=2.0, **kwargs):
    """Draw a 2-sigma covariance ellipse for class x, y."""
    cov = np.cov(x, y)
    pearson = cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1])
    rx = np.sqrt(1 + pearson)
    ry = np.sqrt(1 - pearson)
    ell = Ellipse((0, 0), width=rx * 2, height=ry * 2, **kwargs)
    transf = (transforms.Affine2D()
              .rotate_deg(45)
              .scale(np.sqrt(cov[0, 0]) * n_std,
                     np.sqrt(cov[1, 1]) * n_std)
              .translate(np.mean(x), np.mean(y)))
    ell.set_transform(transf + ax.transData)
    return ax.add_patch(ell)

# ─────────────────────────────────────────────
# 7. VISUALISATIONS  (2 × 3 grid)
# ─────────────────────────────────────────────
COLORS = {
    "Iris-setosa":     "#1B4F72",
    "Iris-versicolor": "#D97706",
    "Iris-virginica":  "#15803D",
}
SHORT = {sp: sp.replace("Iris-", "").capitalize() for sp in le.classes_}
CLIST = [COLORS[sp] for sp in le.classes_]

fig = plt.figure(figsize=(18, 11))
fig.patch.set_facecolor("#F8F7F4")
fig.suptitle(
    "Iris Dataset — SVM Linear Kernel  |  MSE803 Data Analytics  |  Week 6 Activity 1",
    fontsize=14, fontweight="bold", y=0.99, color="#1C1C1C"
)

axes = [fig.add_subplot(2, 3, i) for i in range(1, 7)]
for ax in axes:
    ax.set_facecolor("#F8F7F4")

# ── Plot 1: Sepal scatter + 2σ confidence ellipses ─────────────────────────
ax1 = axes[0]
for sp, grp in df.groupby("species"):
    ax1.scatter(grp["sepal_length"], grp["sepal_width"],
                label=SHORT[sp], color=COLORS[sp],
                alpha=0.75, edgecolors="white", linewidths=0.5, s=55, zorder=3)
    confidence_ellipse(grp["sepal_length"].values, grp["sepal_width"].values,
                       ax1, n_std=2.0,
                       edgecolor=COLORS[sp], facecolor=COLORS[sp],
                       alpha=0.12, linewidth=1.5, linestyle="--")
ax1.set_xlabel("Sepal Length (cm)", fontsize=10)
ax1.set_ylabel("Sepal Width (cm)", fontsize=10)
ax1.set_title("Sepal Dimensions + 2σ Ellipses", fontweight="bold")
ax1.legend(fontsize=8, framealpha=0.6)
ax1.grid(True, alpha=0.25, linestyle=":")

# ── Plot 2: Petal scatter + SVM linear decision boundary ───────────────────
ax2 = axes[1]
x_min = X_tr_2d[:, 0].min() - 0.6
x_max = X_tr_2d[:, 0].max() + 0.6
y_min = X_tr_2d[:, 1].min() - 0.6
y_max = X_tr_2d[:, 1].max() + 0.6
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 400),
                     np.linspace(y_min, y_max, 400))
Z = svm_2d.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

region_colors = ["#D0E4F5", "#FDE9C8", "#C8EBD5"]
ax2.contourf(xx, yy, Z, alpha=0.30, colors=region_colors, levels=[-0.5, 0.5, 1.5, 2.5])
ax2.contour(xx, yy, Z, colors="#555555", linewidths=0.7, alpha=0.6,
            levels=[0.5, 1.5])

for i, sp in enumerate(le.classes_):
    mask = y_train == i
    ax2.scatter(X_tr_2d[mask, 0], X_tr_2d[mask, 1],
                color=COLORS[sp], alpha=0.75, edgecolors="white",
                linewidths=0.5, s=52, zorder=3, label=SHORT[sp])

sv = svm_2d.support_vectors_
ax2.scatter(sv[:, 0], sv[:, 1], s=130, facecolors="none",
            edgecolors="#CC0000", linewidths=1.6, zorder=5,
            label="Support vectors")
acc_2d = svm_2d.score(X_train_sc[:, [2, 3]], y_train)   # train acc of 2D viz model
acc_2d_test = svm_2d.score(X_test_sc[:, [2, 3]], y_test)
ax2.set_xlabel("Petal Length (scaled)", fontsize=10)
ax2.set_ylabel("Petal Width (scaled)", fontsize=10)
ax2.set_title(
    f"Petal Space: Linear SVM Decision Boundary\n"
    f"(2-feature visualisation model — test acc: {acc_2d_test*100:.1f}%)",
    fontweight="bold", fontsize=9.5
)
ax2.legend(fontsize=8, framealpha=0.6)
ax2.grid(True, alpha=0.25, linestyle=":")

# ── Plot 3: Pearson Correlation Heatmap (labels via index rename, no warning) ─
ax3 = axes[2]
label_map = {
    "sepal_length": "Sepal L",
    "sepal_width":  "Sepal W",
    "petal_length": "Petal L",
    "petal_width":  "Petal W",
}
corr = (df[["sepal_length", "sepal_width", "petal_length", "petal_width"]]
        .rename(columns=label_map)
        .corr(method="pearson"))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0,
            linewidths=0.8, ax=ax3,
            annot_kws={"size": 12, "weight": "bold"},
            xticklabels=corr.columns, yticklabels=corr.index)
ax3.set_title("Pearson Correlation Heatmap", fontweight="bold")
ax3.tick_params(axis="x", rotation=25, labelsize=9)
ax3.tick_params(axis="y", rotation=0,  labelsize=9)

# ── Plot 4: SVM coefficient heatmap (OVO pairs × features) ─────────────────
ax4 = axes[3]
pair_labels = ["setosa\nvs\nversicolor",
               "setosa\nvs\nvirginica",
               "versicolor\nvs\nvirginica"]
feat_labels = ["Sepal L", "Sepal W", "Petal L", "Petal W"]
coef_df = pd.DataFrame(svm.coef_, index=pair_labels, columns=feat_labels)
# Use SIGNED values for BOTH color and annotation so the heatmap is consistent
sns.heatmap(coef_df, annot=coef_df.round(3), fmt=".3f",
            cmap="coolwarm", center=0, ax=ax4,
            linewidths=0.6,
            annot_kws={"size": 10, "weight": "bold"},
            xticklabels=feat_labels, yticklabels=pair_labels,
            cbar_kws={"label": "Coefficient value"})
ax4.set_title("SVM Linear Coefficients\n(signed — red=positive push, blue=negative push per OVO pair)",
              fontweight="bold", fontsize=9.0)
ax4.tick_params(axis="x", rotation=0, labelsize=9)
ax4.tick_params(axis="y", rotation=0, labelsize=8)

# ── Plot 5: Confusion Matrix ────────────────────────────────────────────────
ax5 = axes[4]
disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=[SHORT[sp] for sp in le.classes_]
)
disp.plot(ax=ax5, colorbar=False, cmap="Blues")
ax5.set_title("Confusion Matrix — Test Set (n=30)", fontweight="bold")
# Annotate accuracy
ax5.text(0.5, -0.12, f"Overall Accuracy: {acc*100:.1f}%",
         ha="center", va="top", transform=ax5.transAxes,
         fontsize=11, fontweight="bold", color="#15803D")

# ── Plot 6: Violin — all 4 features by species ─────────────────────────────
ax6 = axes[5]
df_m = df.melt(
    id_vars=["species"],
    value_vars=["sepal_length", "sepal_width", "petal_length", "petal_width"],
    var_name="feature", value_name="value"
)
df_m["feature"] = df_m["feature"].map(label_map)
df_m["species_short"] = df_m["species"].map(SHORT)

sns.violinplot(
    data=df_m, x="feature", y="value", hue="species_short",
    ax=ax6, palette=list(COLORS.values()),
    inner="quartile", linewidth=0.9, alpha=0.8,
    order=["Sepal L", "Sepal W", "Petal L", "Petal W"],
    hue_order=[SHORT[sp] for sp in le.classes_]
)
ax6.set_xlabel("Feature", fontsize=10)
ax6.set_ylabel("Value (cm)", fontsize=10)
ax6.set_title("Feature Distributions by Species (Violin)", fontweight="bold")
ax6.legend(title="Species", fontsize=8, title_fontsize=8, framealpha=0.6)
ax6.grid(True, alpha=0.25, axis="y", linestyle=":")

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig("week6_activity1_results.png", dpi=150, bbox_inches="tight",
            facecolor=fig.get_facecolor())
plt.show()
print("\nPlot saved → week6_activity1_results.png")
