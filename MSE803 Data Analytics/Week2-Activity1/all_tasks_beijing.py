import pandas as pd
import glob
import os

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "**", "PRSA_Data_*.csv")
all_files = glob.glob(path, recursive=True)

if not all_files:
    print("CSV files not found. Make sure the PRSA_Data_*.csv files are in the folder.")
    exit()

df = pd.concat([pd.read_csv(f) for f in sorted(all_files)], ignore_index=True)


# ---------------------------------------------------------------
# Task 1 - Load and Inspect the Dataset
# ---------------------------------------------------------------

print("\nTask 1 - Load and Inspect the Dataset")
print("-" * 45)

print(f"\nLoaded {len(all_files)} station files successfully.")
print(f"Combined dataset has {df.shape[0]:,} rows and {df.shape[1]} columns.\n")

print("First 5 rows:")
print(df.head().to_string())

print("\nColumn names and data types:")
dtype_info = pd.DataFrame({
    "Column": df.columns,
    "Data Type": df.dtypes.astype(str).values,
    "Non-Null Count": df.notnull().sum().values,
    "Null Count": df.isnull().sum().values
})
print(dtype_info.to_string(index=False))

print(f"\nDataset shape: {df.shape[0]:,} rows x {df.shape[1]} columns")


# ---------------------------------------------------------------
# Task 2 - Data Cleaning
# ---------------------------------------------------------------

print("\n\nTask 2 - Data Cleaning")
print("-" * 45)

print("\nMissing values before cleaning:")
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
missing_summary = pd.DataFrame({
    "Column": missing.index,
    "Missing Values": missing.values,
    "Missing %": missing_pct.values
})
missing_summary = missing_summary[missing_summary["Missing Values"] > 0]
print(missing_summary.to_string(index=False))
print(f"\nTotal missing values: {df.isnull().sum().sum():,} out of {df.size:,} cells")

# fill pollutant and weather columns with the median per station
# using per-station median rather than overall median because
# pollution levels vary a lot between stations
numeric_cols = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3",
                "TEMP", "PRES", "DEWP", "RAIN", "WSPM"]

for col in numeric_cols:
    df[col] = df.groupby("station")[col].transform(lambda x: x.fillna(x.median()))

# wind direction filled with mode per station
df["wd"] = df.groupby("station")["wd"].transform(lambda x: x.fillna(x.mode()[0]))

print("\nFilled missing values:")
print("  - Numeric columns (PM2.5, PM10, SO2, NO2, CO, O3, TEMP, PRES, DEWP, RAIN, WSPM)")
print("    -> filled with per-station median")
print("  - Wind direction (wd)")
print("    -> filled with per-station mode (most common wind direction)")

remaining_nulls = df.isnull().sum().sum()
if remaining_nulls > 0:
    before = len(df)
    df.dropna(inplace=True)
    print(f"\nDropped {before - len(df)} rows that still had nulls after filling.")
else:
    print(f"\nNo rows dropped - all missing values were filled successfully.")

print(f"\nMissing values after cleaning: {df.isnull().sum().sum()}")
print(f"Final dataset shape: {df.shape[0]:,} rows x {df.shape[1]} columns")


# ---------------------------------------------------------------
# Task 3 - Basic Statistical Analysis
# ---------------------------------------------------------------

print("\n\nTask 3 - Basic Statistical Analysis")
print("-" * 45)

cols_to_analyse = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3",
                   "TEMP", "PRES", "DEWP", "RAIN", "WSPM"]

print("\nStatistics for all numeric columns:")
stats = df[cols_to_analyse].agg(["mean", "median", "min", "max", "std"]).round(2)
stats.index = ["Mean", "Median", "Min", "Max", "Std Dev"]
print(stats.to_string())

print("\nPM2.5 breakdown by station (sorted by mean):")
pm25_by_station = df.groupby("station")["PM2.5"].agg(
    Mean="mean",
    Median="median",
    Min="min",
    Max="max",
    StdDev="std"
).round(2).sort_values("Mean", ascending=False)
print(pm25_by_station.to_string())

print("\nDone.")
