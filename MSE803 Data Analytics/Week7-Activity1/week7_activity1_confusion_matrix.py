import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

# Confusion matrix values
# Test set: 30 records (15 healthy, 15 sick)
# 3 misclassifications: 2 FN, 1 FP
TN = 14   # Healthy correctly predicted as Healthy
FP = 1    # Healthy incorrectly predicted as Sick
FN = 2    # Sick incorrectly predicted as Healthy
TP = 13   # Sick correctly predicted as Sick

total = TN + FP + FN + TP  # 30

# Evaluation metrics
accuracy    = (TP + TN) / total
precision   = TP / (TP + FP)
recall      = TP / (TP + FN)       # Sensitivity
specificity = TN / (TN + FP)
f1          = 2 * (precision * recall) / (precision + recall)

print("Confusion Matrix Values")
print(f"  TN = {TN}  |  FP = {FP}")
print(f"  FN = {FN}  |  TP = {TP}")
print(f"\nEvaluation Metrics")
print(f"  Accuracy    : {accuracy*100:.1f}%")
print(f"  Precision   : {precision*100:.1f}%")
print(f"  Recall      : {recall*100:.1f}%")
print(f"  Specificity : {specificity*100:.1f}%")
print(f"  F1-Score    : {f1*100:.1f}%")

# Colour scheme
GREEN_CORRECT = "#1A5C38"
GREEN_LIGHT   = "#D4EDDA"
RED_WRONG     = "#8B1A1A"
RED_LIGHT     = "#FADADD"
BG            = "#F7F6F3"
DARK          = "#1C1C1C"
MUTED         = "#6B7280"

fig = plt.figure(figsize=(14, 8))
fig.patch.set_facecolor(BG)
fig.suptitle(
    "Healthcare ML Model — Confusion Matrix\nMSE803 Data Analytics  |  Week 7 Activity 1",
    fontsize=14, fontweight="bold", color=DARK, y=0.97
)

# Main layout: confusion matrix on left, metrics on right
gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1], wspace=0.08)
ax_cm  = fig.add_subplot(gs[0])
ax_met = fig.add_subplot(gs[1])
ax_cm.set_facecolor(BG)
ax_met.set_facecolor(BG)

# Draw confusion matrix as coloured cells
cells = [
    # (row, col, value, fill_color, text_color, label, sublabel)
    (0, 0, TN, GREEN_LIGHT, GREEN_CORRECT, "TRUE NEGATIVE",  "Healthy → Healthy\n(correct)"),
    (0, 1, FP, RED_LIGHT,   RED_WRONG,     "FALSE POSITIVE", "Healthy → Sick\n(incorrect)"),
    (1, 0, FN, RED_LIGHT,   RED_WRONG,     "FALSE NEGATIVE", "Sick → Healthy\n(incorrect)"),
    (1, 1, TP, GREEN_LIGHT, GREEN_CORRECT, "TRUE POSITIVE",  "Sick → Sick\n(correct)"),
]

cell_size = 1.0
gap = 0.04

for (row, col, val, fill, text_col, label, sublabel) in cells:
    x = col * (cell_size + gap)
    y = (1 - row) * (cell_size + gap)

    rect = mpatches.FancyBboxPatch(
        (x, y), cell_size, cell_size,
        boxstyle="round,pad=0.02",
        facecolor=fill,
        edgecolor=text_col,
        linewidth=2.2
    )
    ax_cm.add_patch(rect)

    # Large number
    ax_cm.text(x + cell_size / 2, y + cell_size * 0.58,
               str(val),
               ha="center", va="center",
               fontsize=48, fontweight="bold",
               color=text_col)

    # Label (TN / FP / FN / TP)
    ax_cm.text(x + cell_size / 2, y + cell_size * 0.82,
               label,
               ha="center", va="center",
               fontsize=8.5, fontweight="bold",
               color=text_col, alpha=0.85)

    # Sub-label
    ax_cm.text(x + cell_size / 2, y + cell_size * 0.28,
               sublabel,
               ha="center", va="center",
               fontsize=8, color=MUTED,
               linespacing=1.5)

# Axis labels
ax_cm.text(cell_size / 2 + (cell_size + gap) / 2, -0.18,
           "Predicted Label", ha="center", fontsize=11, fontweight="bold", color=DARK)
ax_cm.text(cell_size / 2, 2 * cell_size + gap + 0.2,
           "Healthy", ha="center", fontsize=10, color=DARK)
ax_cm.text(cell_size / 2 + cell_size + gap, 2 * cell_size + gap + 0.2,
           "Sick", ha="center", fontsize=10, color=DARK)

ax_cm.text(-0.25, cell_size + gap / 2,
           "Actual\nLabel", ha="center", va="center",
           fontsize=11, fontweight="bold", color=DARK, rotation=90)
ax_cm.text(-0.08, 1.5 * cell_size + gap,
           "Healthy", ha="center", va="center",
           fontsize=10, color=DARK, rotation=90)
ax_cm.text(-0.08, 0.5 * cell_size,
           "Sick", ha="center", va="center",
           fontsize=10, color=DARK, rotation=90)

# Total row/column labels
ax_cm.text(cell_size / 2, -0.08,
           "n=15", ha="center", fontsize=8.5, color=MUTED)
ax_cm.text(cell_size / 2 + cell_size + gap, -0.08,
           "n=15", ha="center", fontsize=8.5, color=MUTED)

ax_cm.set_xlim(-0.4, 2 * cell_size + gap + 0.15)
ax_cm.set_ylim(-0.35, 2 * cell_size + gap + 0.4)
ax_cm.axis("off")

# Metrics panel
ax_met.axis("off")

metrics = [
    ("Accuracy",    accuracy,    "#1A5C38", "Overall correct predictions out of 30"),
    ("Precision",   precision,   "#1A5C38", "Of those predicted Sick, how many were Sick"),
    ("Recall",      recall,      "#8B1A1A", "Of actual Sick, how many were caught"),
    ("Specificity", specificity, "#1A5C38", "Of actual Healthy, how many were correct"),
    ("F1-Score",    f1,          "#1A5876", "Harmonic mean of Precision and Recall"),
]

ax_met.text(0.5, 0.97, "Evaluation Metrics", ha="center", va="top",
            fontsize=12, fontweight="bold", color=DARK,
            transform=ax_met.transAxes)
ax_met.plot([0.05, 0.95], [0.925, 0.925], color=MUTED, linewidth=0.7, alpha=0.5,
            transform=ax_met.transAxes, clip_on=False)

for i, (name, val, col, desc) in enumerate(metrics):
    y_pos = 0.87 - i * 0.165

    # Bar background
    bar_bg = mpatches.FancyBboxPatch(
        (0.05, y_pos - 0.035), 0.9, 0.115,
        boxstyle="round,pad=0.01",
        facecolor="white", edgecolor="#E5E7EB",
        linewidth=1, transform=ax_met.transAxes, clip_on=False
    )
    ax_met.add_patch(bar_bg)

    # Filled progress bar
    bar_fill = mpatches.FancyBboxPatch(
        (0.05, y_pos - 0.035), 0.9 * val, 0.115,
        boxstyle="round,pad=0.01",
        facecolor=col, alpha=0.15,
        edgecolor="none",
        transform=ax_met.transAxes, clip_on=False
    )
    ax_met.add_patch(bar_fill)

    ax_met.text(0.08, y_pos + 0.038, name, ha="left", va="center",
                fontsize=10.5, fontweight="bold", color=col,
                transform=ax_met.transAxes)
    ax_met.text(0.92, y_pos + 0.038, f"{val*100:.1f}%", ha="right", va="center",
                fontsize=13, fontweight="bold", color=col,
                transform=ax_met.transAxes)
    ax_met.text(0.08, y_pos - 0.01, desc, ha="left", va="center",
                fontsize=7.5, color=MUTED,
                transform=ax_met.transAxes)

# Key finding note
note_box = mpatches.FancyBboxPatch(
    (0.05, 0.03), 0.9, 0.09,
    boxstyle="round,pad=0.015",
    facecolor=RED_LIGHT, edgecolor=RED_WRONG,
    linewidth=1.2, transform=ax_met.transAxes, clip_on=False
)
ax_met.add_patch(note_box)
ax_met.text(0.5, 0.095, "Clinical Note", ha="center", va="center",
            fontsize=8.5, fontweight="bold", color=RED_WRONG,
            transform=ax_met.transAxes)
ax_met.text(0.5, 0.06, "2 False Negatives are high-risk: sick patients sent home.",
            ha="center", va="center",
            fontsize=8, color=RED_WRONG,
            transform=ax_met.transAxes)

plt.savefig("week7_activity1_confusion_matrix.png", dpi=150,
            bbox_inches="tight", facecolor=BG)
plt.show()
print("Saved: week7_activity1_confusion_matrix.png")
