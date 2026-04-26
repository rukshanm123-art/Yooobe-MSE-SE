import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import glob, os

sns.set_theme(style="whitegrid", palette="muted")
OUT = "/tmp/beijing_air/charts"
os.makedirs(OUT, exist_ok=True)

# ─── Load ───────────────────────────────────────────────────────────────────
path = "/tmp/beijing_air/PRSA_Data_20130301-20170228/PRSA_Data_*.csv"
all_files = sorted(glob.glob(path))
df = pd.concat([pd.read_csv(f) for f in all_files], ignore_index=True)

print("\n=== TASK 1 – Load and Inspect the Dataset ===")
print(f"Loaded {len(all_files)} station files.")
print(f"Combined shape: {df.shape[0]:,} rows × {df.shape[1]} columns\n")
print("First 5 rows:")
print(df.head().to_string())
print("\nColumn names and data types:")
dtype_info = pd.DataFrame({
    "Column": df.columns,
    "Data Type": df.dtypes.astype(str).values,
    "Non-Null": df.notnull().sum().values,
    "Null": df.isnull().sum().values
})
print(dtype_info.to_string(index=False))

# ─── Task 2 – Data Cleaning ──────────────────────────────────────────────────
print("\n\n=== TASK 2 – Data Cleaning ===")
print("Missing values before cleaning:")
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
ms = pd.DataFrame({"Column": missing.index, "Missing": missing.values, "%": missing_pct.values})
print(ms[ms["Missing"] > 0].to_string(index=False))
print(f"\nTotal missing: {df.isnull().sum().sum():,} / {df.size:,} cells")

numeric_cols = ["PM2.5","PM10","SO2","NO2","CO","O3","TEMP","PRES","DEWP","RAIN","WSPM"]
for col in numeric_cols:
    df[col] = df.groupby("station")[col].transform(lambda x: x.fillna(x.median()))
df["wd"] = df.groupby("station")["wd"].transform(lambda x: x.fillna(x.mode()[0]))

remaining = df.isnull().sum().sum()
if remaining:
    before = len(df)
    df.dropna(inplace=True)
    print(f"Dropped {before - len(df)} rows still containing nulls.")
print(f"Missing after cleaning: {df.isnull().sum().sum()}")
print(f"Final shape: {df.shape[0]:,} rows × {df.shape[1]} columns")

# ─── Task 3 – Basic Statistical Analysis ─────────────────────────────────────
print("\n\n=== TASK 3 – Basic Statistical Analysis ===")
cols_stat = ["PM2.5","PM10","SO2","NO2","CO","O3","TEMP","PRES","DEWP","RAIN","WSPM"]
stats = df[cols_stat].agg(["mean","median","min","max","std"]).round(2)
stats.index = ["Mean","Median","Min","Max","Std Dev"]
print(stats.to_string())

print("\nPM2.5 by station (sorted by mean):")
pm25_stn = df.groupby("station")["PM2.5"].agg(
    Mean="mean", Median="median", Min="min", Max="max", StdDev="std"
).round(2).sort_values("Mean", ascending=False)
print(pm25_stn.to_string())

# save stats to CSV for reference
stats.to_csv(f"{OUT}/task3_stats.csv")
pm25_stn.to_csv(f"{OUT}/task3_pm25_by_station.csv")

# ─── Task 4 – Data Visualisation ─────────────────────────────────────────────
print("\n\n=== TASK 4 – Data Visualisation ===")

# 4a – PM2.5 distribution by station (box plot)
fig, ax = plt.subplots(figsize=(12, 5))
stations_ordered = df.groupby("station")["PM2.5"].median().sort_values(ascending=False).index
df_plot = df[df["station"].isin(stations_ordered)]
df_plot["station"] = pd.Categorical(df_plot["station"], categories=stations_ordered, ordered=True)
df_plot.sort_values("station", inplace=True)
sns.boxplot(data=df_plot, x="station", y="PM2.5", ax=ax, showfliers=False, palette="Spectral")
ax.set_title("PM2.5 Distribution by Station (Outliers Hidden)", fontsize=13, fontweight="bold")
ax.set_xlabel("Station"); ax.set_ylabel("PM2.5 (µg/m³)")
ax.tick_params(axis="x", rotation=30)
plt.tight_layout()
plt.savefig(f"{OUT}/task4a_pm25_boxplot.png", dpi=120)
plt.close()
print("Saved task4a_pm25_boxplot.png")

# 4b – Monthly average PM2.5 (line chart)
df["date"] = pd.to_datetime(df[["year","month","day"]])
monthly = df.groupby(df["date"].dt.to_period("M"))["PM2.5"].mean().reset_index()
monthly["date"] = monthly["date"].dt.to_timestamp()
fig, ax = plt.subplots(figsize=(13, 4))
ax.plot(monthly["date"], monthly["PM2.5"], color="steelblue", linewidth=1.2)
ax.fill_between(monthly["date"], monthly["PM2.5"], alpha=0.2, color="steelblue")
ax.set_title("Monthly Average PM2.5 Across All Stations (2013–2017)", fontsize=13, fontweight="bold")
ax.set_xlabel("Date"); ax.set_ylabel("PM2.5 (µg/m³)")
ax.xaxis.set_major_locator(ticker.MaxNLocator(10))
plt.xticks(rotation=30); plt.tight_layout()
plt.savefig(f"{OUT}/task4b_pm25_monthly.png", dpi=120)
plt.close()
print("Saved task4b_pm25_monthly.png")

# 4c – Average PM2.5 by hour of day
hourly = df.groupby("hour")["PM2.5"].mean()
fig, ax = plt.subplots(figsize=(9, 4))
ax.bar(hourly.index, hourly.values, color="coral", edgecolor="white")
ax.set_title("Average PM2.5 by Hour of Day", fontsize=13, fontweight="bold")
ax.set_xlabel("Hour (0–23)"); ax.set_ylabel("PM2.5 (µg/m³)")
ax.set_xticks(range(0, 24))
plt.tight_layout()
plt.savefig(f"{OUT}/task4c_pm25_hourly.png", dpi=120)
plt.close()
print("Saved task4c_pm25_hourly.png")

# 4d – Average PM2.5 by season
df["season"] = df["month"].map({12:"Winter",1:"Winter",2:"Winter",
                                 3:"Spring",4:"Spring",5:"Spring",
                                 6:"Summer",7:"Summer",8:"Summer",
                                 9:"Autumn",10:"Autumn",11:"Autumn"})
season_order = ["Spring","Summer","Autumn","Winter"]
season_avg = df.groupby("season")["PM2.5"].mean().reindex(season_order)
colors = ["#a8d5a2","#f6d365","#e8a87c","#84b9cb"]
fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(season_avg.index, season_avg.values, color=colors, edgecolor="white", width=0.55)
for bar, val in zip(bars, season_avg.values):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1, f"{val:.1f}", ha="center", fontsize=10)
ax.set_title("Average PM2.5 by Season", fontsize=13, fontweight="bold")
ax.set_ylabel("PM2.5 (µg/m³)")
plt.tight_layout()
plt.savefig(f"{OUT}/task4d_pm25_season.png", dpi=120)
plt.close()
print("Saved task4d_pm25_season.png")

# 4e – Per-station mean PM2.5 bar chart
fig, ax = plt.subplots(figsize=(11, 4))
stn_mean = df.groupby("station")["PM2.5"].mean().sort_values(ascending=False)
palette = sns.color_palette("Spectral", len(stn_mean))
bars = ax.bar(stn_mean.index, stn_mean.values, color=palette, edgecolor="white")
for bar, val in zip(bars, stn_mean.values):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5, f"{val:.0f}", ha="center", fontsize=8)
ax.set_title("Mean PM2.5 by Station", fontsize=13, fontweight="bold")
ax.set_ylabel("PM2.5 (µg/m³)")
ax.tick_params(axis="x", rotation=35)
plt.tight_layout()
plt.savefig(f"{OUT}/task4e_pm25_station_bar.png", dpi=120)
plt.close()
print("Saved task4e_pm25_station_bar.png")

# ─── Task 5 – Correlation Analysis ───────────────────────────────────────────
print("\n\n=== TASK 5 – Correlation Analysis ===")
corr_cols = ["PM2.5","PM10","SO2","NO2","CO","O3","TEMP","PRES","DEWP","RAIN","WSPM"]
corr = df[corr_cols].corr().round(2)
print(corr.to_string())

# 5a – Heatmap
fig, ax = plt.subplots(figsize=(10, 8))
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm",
            center=0, linewidths=0.5, ax=ax, cbar_kws={"shrink": 0.7})
ax.set_title("Correlation Matrix – Air Quality & Weather Variables", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{OUT}/task5a_correlation_heatmap.png", dpi=120)
plt.close()
print("Saved task5a_correlation_heatmap.png")

# 5b – PM2.5 vs TEMP scatter
fig, ax = plt.subplots(figsize=(7, 5))
sample = df.sample(5000, random_state=42)
ax.scatter(sample["TEMP"], sample["PM2.5"], alpha=0.25, s=8, color="steelblue")
m, b = np.polyfit(df["TEMP"], df["PM2.5"], 1)
x_line = np.linspace(df["TEMP"].min(), df["TEMP"].max(), 200)
ax.plot(x_line, m*x_line+b, color="red", linewidth=1.5, label=f"y={m:.2f}x+{b:.1f}")
ax.set_title("PM2.5 vs Temperature", fontsize=13, fontweight="bold")
ax.set_xlabel("Temperature (°C)"); ax.set_ylabel("PM2.5 (µg/m³)")
ax.legend()
plt.tight_layout()
plt.savefig(f"{OUT}/task5b_pm25_vs_temp.png", dpi=120)
plt.close()
print("Saved task5b_pm25_vs_temp.png")

# 5c – PM2.5 vs WSPM scatter
fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(sample["WSPM"], sample["PM2.5"], alpha=0.25, s=8, color="darkorange")
m2, b2 = np.polyfit(df["WSPM"], df["PM2.5"], 1)
x2 = np.linspace(df["WSPM"].min(), df["WSPM"].max(), 200)
ax.plot(x2, m2*x2+b2, color="red", linewidth=1.5, label=f"y={m2:.2f}x+{b2:.1f}")
ax.set_title("PM2.5 vs Wind Speed", fontsize=13, fontweight="bold")
ax.set_xlabel("Wind Speed (m/s)"); ax.set_ylabel("PM2.5 (µg/m³)")
ax.legend()
plt.tight_layout()
plt.savefig(f"{OUT}/task5c_pm25_vs_wspm.png", dpi=120)
plt.close()
print("Saved task5c_pm25_vs_wspm.png")

# ─── Task 6 – Conclusions & Insights ─────────────────────────────────────────
print("\n\n=== TASK 6 – Conclusions & Insights ===")

# WHO guideline for PM2.5 annual mean = 5 µg/m³ (2021 revision)
who_limit = 5.0
stn_annual = df.groupby("station")["PM2.5"].mean().round(2)
print(f"WHO annual PM2.5 guideline: {who_limit} µg/m³")
print("All stations exceed the WHO guideline:")
for stn, val in stn_annual.sort_values(ascending=False).items():
    times = val / who_limit
    print(f"  {stn}: {val} µg/m³  ({times:.1f}× WHO limit)")

worst_stn = stn_annual.idxmax()
best_stn  = stn_annual.idxmin()
highest_corr = corr["PM2.5"].drop("PM2.5").abs().idxmax()
print(f"\nHighest-pollution station: {worst_stn} ({stn_annual[worst_stn]} µg/m³)")
print(f"Lowest-pollution  station: {best_stn}  ({stn_annual[best_stn]} µg/m³)")
print(f"Strongest correlate with PM2.5: {highest_corr} (r={corr.loc['PM2.5', highest_corr]})")

winter_pm = df[df["season"]=="Winter"]["PM2.5"].mean()
summer_pm = df[df["season"]=="Summer"]["PM2.5"].mean()
print(f"\nWinter mean PM2.5: {winter_pm:.1f} µg/m³")
print(f"Summer mean PM2.5: {summer_pm:.1f} µg/m³")
print(f"Winter is {winter_pm/summer_pm:.1f}× higher than Summer")

print("\nDone – all charts saved to", OUT)
