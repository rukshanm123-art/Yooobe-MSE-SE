import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import seaborn as sns
from matplotlib.patches import Ellipse
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay


# Load dataset
cols = ["sepal_length", "sepal_width", "petal_length", "petal_width", "species"]
df = pd.read_csv("iris.data", header=None, names=cols)

print("Iris Dataset Overview")
print(df.head(10).to_string())
print(f"\nShape: {df.shape}")
print(f"Classes: {df['species'].unique()}")

# Data cleaning
print("\nMissing values:")
print(df.isnull().sum())
print(f"\nDuplicate rows: {df.duplicated().sum()}")
df = df.drop_duplicates()
print(f"Shape after removing duplicates: {df.shape}")
print("\nClass distribution:")
print(df["species"].value_counts())
print("\nDescriptive statistics:")
print(df.describe().round(3))

# Encode labels and split
le = LabelEncoder()
df["label"] = le.fit_transform(df["species"])

X = df[["sepal_length", "sepal_width", "petal_length", "petal_width"]].values
y = df["label"].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc = scaler.transform(X_test)

print(f"\nTraining samples: {len(X_train)} | Test samples: {len(X_test)}")

# Train SVM with linear kernel
svm = SVC(kernel="linear", C=1.0, random_state=42)
svm.fit(X_train_sc, y_train)
y_pred = svm.predict(X_test_sc)

acc = accuracy_score(y_test, y_pred)
report_dict = classification_report(y_test, y_pred, target_names=le.classes_, output_dict=True)
cm = confusion_matrix(y_test, y_pred)

print("\nSVM Linear Kernel - Evaluation Metrics (Test Set)")
print(f"Accuracy: {acc:.4f} ({acc * 100:.2f}%)")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=le.classes_))
print("Confusion Matrix:")
print(cm)

# Train a 2D SVM on petal features only for the decision boundary visualisation
svm_2d = SVC(kernel="linear", C=1.0, random_state=42)
X_train_petal = X_train_sc[:, [2, 3]]
svm_2d.fit(X_train_petal, y_train)
acc_2d_test = svm_2d.score(X_test_sc[:, [2, 3]], y_test)


def confidence_ellipse(x, y, ax, n_std=2.0, **kwargs):
    """Plot a 2-sigma confidence ellipse based on the covariance of x and y."""
    cov = np.cov(x, y)
    pearson = cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1])
    rx = np.sqrt(1 + pearson)
    ry = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=rx * 2, height=ry * 2, **kwargs)
    transf = (transforms.Affine2D()
              .rotate_deg(45)
              .scale(np.sqrt(cov[0, 0]) * n_std, np.sqrt(cov[1, 1]) * n_std)
              .translate(np.mean(x), np.mean(y)))
    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)


# Colour palette and short species names
colors = {
    "Iris-setosa":     "#1B4F72",
    "Iris-versicolor": "#D97706",
    "Iris-virginica":  "#15803D",
}
short_name = {sp: sp.replace("Iris-", "").capitalize() for sp in le.classes_}

label_map = {
    "sepal_length": "Sepal L",
    "sepal_width":  "Sepal W",
    "petal_length": "Petal L",
    "petal_width":  "Petal W",
}

fig = plt.figure(figsize=(18, 11))
fig.patch.set_facecolor("#F8F7F4")
fig.suptitle(
    "Iris Dataset — SVM Linear Kernel  |  MSE803 Data Analytics  |  Week 6 Activity 1",
    fontsize=14, fontweight="bold", y=0.99, color="#1C1C1C"
)

axes = [fig.add_subplot(2, 3, i) for i in range(1, 7)]
for ax in axes:
    ax.set_facecolor("#F8F7F4")

# Plot 1: Sepal scatter with 2-sigma confidence ellipses per class
ax1 = axes[0]
for sp, grp in df.groupby("species"):
    ax1.scatter(grp["sepal_length"], grp["sepal_width"],
                label=short_name[sp], color=colors[sp],
                alpha=0.75, edgecolors="white", linewidths=0.5, s=55, zorder=3)
    confidence_ellipse(grp["sepal_length"].values, grp["sepal_width"].values,
                       ax1, n_std=2.0, edgecolor=colors[sp], facecolor=colors[sp],
                       alpha=0.12, linewidth=1.5, linestyle="--")
ax1.set_xlabel("Sepal Length (cm)", fontsize=10)
ax1.set_ylabel("Sepal Width (cm)", fontsize=10)
ax1.set_title("Sepal Dimensions + 2σ Ellipses", fontweight="bold")
ax1.legend(fontsize=8, framealpha=0.6)
ax1.grid(True, alpha=0.25, linestyle=":")

# Plot 2: Petal scatter with SVM linear decision boundary (2-feature model)
ax2 = axes[1]
x_min = X_train_petal[:, 0].min() - 0.6
x_max = X_train_petal[:, 0].max() + 0.6
y_min = X_train_petal[:, 1].min() - 0.6
y_max = X_train_petal[:, 1].max() + 0.6
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 400), np.linspace(y_min, y_max, 400))
Z = svm_2d.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

region_colors = ["#D0E4F5", "#FDE9C8", "#C8EBD5"]
ax2.contourf(xx, yy, Z, alpha=0.30, colors=region_colors, levels=[-0.5, 0.5, 1.5, 2.5])
ax2.contour(xx, yy, Z, colors="#555555", linewidths=0.7, alpha=0.6, levels=[0.5, 1.5])

for i, sp in enumerate(le.classes_):
    mask = y_train == i
    ax2.scatter(X_train_petal[mask, 0], X_train_petal[mask, 1],
                color=colors[sp], alpha=0.75, edgecolors="white",
                linewidths=0.5, s=52, zorder=3, label=short_name[sp])

sv = svm_2d.support_vectors_
ax2.scatter(sv[:, 0], sv[:, 1], s=130, facecolors="none",
            edgecolors="#CC0000", linewidths=1.6, zorder=5, label="Support vectors")
ax2.set_xlabel("Petal Length (scaled)", fontsize=10)
ax2.set_ylabel("Petal Width (scaled)", fontsize=10)
ax2.set_title(
    f"Petal Space: Linear SVM Decision Boundary\n(2-feature model — test acc: {acc_2d_test * 100:.1f}%)",
    fontweight="bold", fontsize=9.5
)
ax2.legend(fontsize=8, framealpha=0.6)
ax2.grid(True, alpha=0.25, linestyle=":")

# Plot 3: Pearson correlation heatmap
ax3 = axes[2]
corr = (df[["sepal_length", "sepal_width", "petal_length", "petal_width"]]
        .rename(columns=label_map)
        .corr(method="pearson"))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0,
            linewidths=0.8, ax=ax3, annot_kws={"size": 12, "weight": "bold"},
            xticklabels=corr.columns, yticklabels=corr.index)
ax3.set_title("Pearson Correlation Heatmap", fontweight="bold")
ax3.tick_params(axis="x", rotation=25, labelsize=9)
ax3.tick_params(axis="y", rotation=0, labelsize=9)

# Plot 4: SVM linear coefficients per OVO pair (signed values, diverging colourmap)
ax4 = axes[3]
pair_labels = ["setosa\nvs\nversicolor", "setosa\nvs\nvirginica", "versicolor\nvs\nvirginica"]
feat_labels = ["Sepal L", "Sepal W", "Petal L", "Petal W"]
coef_df = pd.DataFrame(svm.coef_, index=pair_labels, columns=feat_labels)
sns.heatmap(coef_df, annot=coef_df.round(3), fmt=".3f",
            cmap="coolwarm", center=0, ax=ax4, linewidths=0.6,
            annot_kws={"size": 10, "weight": "bold"},
            xticklabels=feat_labels, yticklabels=pair_labels,
            cbar_kws={"label": "Coefficient value"})
ax4.set_title("SVM Linear Coefficients\n(red = positive push, blue = negative push per OVO pair)",
              fontweight="bold", fontsize=9.0)
ax4.tick_params(axis="x", rotation=0, labelsize=9)
ax4.tick_params(axis="y", rotation=0, labelsize=8)

# Plot 5: Confusion matrix on the test set
ax5 = axes[4]
disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=[short_name[sp] for sp in le.classes_]
)
disp.plot(ax=ax5, colorbar=False, cmap="Blues")
ax5.set_title("Confusion Matrix — Test Set (n=30)", fontweight="bold")
ax5.text(0.5, -0.12, f"Overall Accuracy: {acc * 100:.1f}%",
         ha="center", va="top", transform=ax5.transAxes,
         fontsize=11, fontweight="bold", color="#15803D")

# Plot 6: Violin plot of all 4 features grouped by species
ax6 = axes[5]
df_melted = df.melt(
    id_vars=["species"],
    value_vars=["sepal_length", "sepal_width", "petal_length", "petal_width"],
    var_name="feature", value_name="value"
)
df_melted["feature"] = df_melted["feature"].map(label_map)
df_melted["species_short"] = df_melted["species"].map(short_name)

sns.violinplot(
    data=df_melted, x="feature", y="value", hue="species_short",
    ax=ax6, palette=list(colors.values()),
    inner="quartile", linewidth=0.9, alpha=0.8,
    order=["Sepal L", "Sepal W", "Petal L", "Petal W"],
    hue_order=[short_name[sp] for sp in le.classes_]
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
print("Plot saved.")
