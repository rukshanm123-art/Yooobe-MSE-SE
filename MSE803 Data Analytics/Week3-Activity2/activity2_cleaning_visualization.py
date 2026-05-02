import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ──────────────────────────────────────────────
# 1. LOAD
# ──────────────────────────────────────────────
df = pd.read_csv('/Users/rukshandesilva/Downloads/messy_dataset_Mukesh.csv')

print("=" * 55)
print("RAW DATASET")
print("=" * 55)
print(df.to_string())
print("\nShape:", df.shape)
print("\nMissing values per column:\n", df.isnull().sum())
print("\nData types:\n", df.dtypes)

# ──────────────────────────────────────────────
# 2. DATA CLEANING
# ──────────────────────────────────────────────

# 2a. Fix text numbers before any type conversion
df['Age'] = df['Age'].replace('thirty-eight', '38')
df['Salary'] = df['Salary'].replace('sixty five thousand', '65000')

# 2b. Convert to numeric
df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
df['Salary'] = pd.to_numeric(df['Salary'], errors='coerce')
df['ID'] = pd.to_numeric(df['ID'], errors='coerce')

# 2c. Handle duplicate ID=2 (Bob appears twice with complementary missing values)
# Merge both rows so we keep Age from row 1 and Salary from row 2
bob_rows = df[df['ID'] == 2]
if len(bob_rows) == 2:
    merged_age    = bob_rows['Age'].dropna().values[0]    if bob_rows['Age'].notna().any()    else np.nan
    merged_salary = bob_rows['Salary'].dropna().values[0] if bob_rows['Salary'].notna().any() else np.nan
    df.loc[df['ID'] == 2, 'Age']    = merged_age
    df.loc[df['ID'] == 2, 'Salary'] = merged_salary
    df = df.drop_duplicates(subset='ID', keep='first')

# 2d. Fix missing ID for Eve (assign next available)
df['ID'] = df['ID'].fillna(df['ID'].max() + 1).astype(int)

# 2e. Standardise country codes (AU → AUS)
df['Country'] = df['Country'].replace('AU', 'AUS')

# 2f. Fill missing Country with mode
df['Country'] = df['Country'].fillna(df['Country'].mode()[0])

# 2g. Parse dates — handle mixed formats and invalid dates
def safe_parse(date_str):
    if pd.isna(date_str):
        return pd.NaT
    for fmt in ('%d/%m/%Y', '%Y-%d-%m', '%Y-%m-%d'):
        try:
            return pd.to_datetime(date_str, format=fmt)
        except (ValueError, TypeError):
            pass
    return pd.NaT  # truly unparseable (e.g. month=13)

df['Join Date'] = df['Join Date'].apply(safe_parse)

# 2h. Fill remaining numeric NaNs with column median
df['Age']    = df['Age'].fillna(df['Age'].median())
df['Salary'] = df['Salary'].fillna(df['Salary'].median())

# 2i. Fill missing Name with 'Unknown'
df['Name'] = df['Name'].fillna('Unknown')

print("\n" + "=" * 55)
print("CLEANED DATASET")
print("=" * 55)
print(df.to_string())
print("\nMissing values after cleaning:\n", df.isnull().sum())

# ──────────────────────────────────────────────
# 3. OUTLIER DETECTION  (IQR method)
# ──────────────────────────────────────────────
print("\n" + "=" * 55)
print("OUTLIER DETECTION (IQR Method)")
print("=" * 55)

for col in ['Age', 'Salary']:
    Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
    outliers = df[(df[col] < lower) | (df[col] > upper)]
    print(f"\n{col}: Q1={Q1}, Q3={Q3}, IQR={IQR}")
    print(f"  Bounds: [{lower:.1f}, {upper:.1f}]")
    if outliers.empty:
        print("  No outliers detected.")
    else:
        print(f"  Outliers:\n{outliers[['ID','Name', col]]}")

# ──────────────────────────────────────────────
# 4. VISUALISATIONS
# ──────────────────────────────────────────────
fig, axes = plt.subplots(2, 3, figsize=(16, 11))
fig.suptitle("Activity 2 — Data Cleaning & Visualisation\nDataset: messy_dataset_Mukesh.csv",
             fontsize=14, fontweight='bold', y=0.98)

numeric_cols = df[['Age', 'Salary']]

# Plot 1: Correlation Heatmap (Pearson)
corr_matrix = numeric_cols.corr(method='pearson')
sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm',
            center=0, linewidths=1, ax=axes[0, 0],
            annot_kws={'size': 14, 'weight': 'bold'})
axes[0, 0].set_title('Pearson Correlation Heatmap', fontweight='bold')

# Plot 2: Scatter plot Age vs Salary with regression line
slope, intercept = np.polyfit(df['Age'], df['Salary'], 1)
x_sorted = np.sort(df['Age'])
reg_line  = slope * x_sorted + intercept
axes[0, 1].scatter(df['Age'], df['Salary'], color='steelblue', edgecolors='white', s=80, zorder=3)
axes[0, 1].plot(x_sorted, reg_line, color='crimson', linewidth=2, label='Regression line')
axes[0, 1].set_xlabel('Age')
axes[0, 1].set_ylabel('Salary')
axes[0, 1].set_title('Age vs Salary (with Regression)', fontweight='bold')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)
r = corr_matrix.loc['Age', 'Salary']
axes[0, 1].annotate(f'r = {r:.3f}', xy=(0.05, 0.92), xycoords='axes fraction',
                    fontsize=11, color='crimson', fontweight='bold')

# Plot 3: Boxplot — outlier visualisation (z-score normalised so both fit one axis)
age_z    = (df['Age']    - df['Age'].mean())    / df['Age'].std()
salary_z = (df['Salary'] - df['Salary'].mean()) / df['Salary'].std()
axes[0, 2].boxplot([age_z, salary_z],
                   tick_labels=['Age (z)', 'Salary (z)'],
                   patch_artist=True,
                   boxprops=dict(facecolor='lightblue'),
                   medianprops=dict(color='crimson', linewidth=2))
axes[0, 2].set_title('Boxplot — Outlier Detection\n(Standardised / Z-score)', fontweight='bold')
axes[0, 2].set_ylabel('Z-score')
axes[0, 2].axhline(0, color='grey', linestyle='--', linewidth=0.8)
axes[0, 2].grid(True, alpha=0.3)

# Plot 4: Age distribution
axes[1, 0].hist(df['Age'], bins=6, color='steelblue', edgecolor='white', alpha=0.85)
axes[1, 0].axvline(df['Age'].mean(), color='crimson', linestyle='--', label=f"Mean: {df['Age'].mean():.1f}")
axes[1, 0].set_title('Age Distribution', fontweight='bold')
axes[1, 0].set_xlabel('Age')
axes[1, 0].set_ylabel('Frequency')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

# Plot 5: Salary distribution
axes[1, 1].hist(df['Salary'], bins=6, color='mediumseagreen', edgecolor='white', alpha=0.85)
axes[1, 1].axvline(df['Salary'].mean(), color='crimson', linestyle='--',
                   label=f"Mean: {df['Salary'].mean():,.0f}")
axes[1, 1].set_title('Salary Distribution', fontweight='bold')
axes[1, 1].set_xlabel('Salary')
axes[1, 1].set_ylabel('Frequency')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

# Plot 6: Country count
country_counts = df['Country'].value_counts()
axes[1, 2].bar(country_counts.index, country_counts.values,
               color=['steelblue', 'mediumseagreen'], edgecolor='white')
axes[1, 2].set_title('Records by Country', fontweight='bold')
axes[1, 2].set_xlabel('Country')
axes[1, 2].set_ylabel('Count')
axes[1, 2].grid(True, alpha=0.3, axis='y')

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('/Users/rukshandesilva/Desktop/activity2_output.png', dpi=150, bbox_inches='tight')
plt.show()
print("\nPlot saved → /Users/rukshandesilva/Desktop/activity2_output.png")
