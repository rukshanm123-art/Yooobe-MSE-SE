# Week 2 – Activity 2: Beijing Air Quality – Statistical Analysis & Presentation

**Course:** MSE803  
**Dataset:** [UCI ML Repository – Beijing Multi-Site Air Quality (ID: 501)](https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality+data)

---

## Overview

This activity extends Activity 1 by completing Tasks 2–6 of the statistical analysis on the Beijing Multi-Site Air Quality dataset, and presenting findings in a PowerPoint presentation.

---

## Tasks Completed

### Task 2 – Data Cleaning
- Identified 74,027 missing values across 12 columns (< 1% of data)
- Numeric columns filled with per-station median
- Wind direction filled with per-station mode
- Result: 0 missing values, 0 rows dropped

### Task 3 – Basic Statistical Analysis
- Summary statistics (mean, median, min, max, std dev) for all pollutant and weather columns
- PM2.5 ranked by station — Dongsi highest (85.66 µg/m³), Dingling lowest (65.43 µg/m³)
- All stations exceed the WHO annual PM2.5 limit of 5 µg/m³ by 13–17x

### Task 4 – Data Visualisation
- Monthly PM2.5 trend line (2013–2017)
- PM2.5 distribution by station (box plot)
- Average PM2.5 by season
- Average PM2.5 by hour of day
- Mean PM2.5 per station (bar chart)

### Task 5 – Correlation Analysis
- Full correlation matrix across all 11 numeric variables
- PM2.5 vs Temperature scatter plot (r = -0.13)
- PM2.5 vs Wind Speed scatter plot (r = -0.27)

### Task 6 – Conclusions
- Winter PM2.5 (94.7 µg/m³) is 1.5x higher than summer (64.5 µg/m³)
- CO is the strongest non-weather predictor of PM2.5 (r = 0.77)
- No improvement in air quality observed over the 2013–2017 period

---

## Files

| File | Description |
|---|---|
| `analysis.py` | Complete Python script — Tasks 1 to 6 |
| `requirements.txt` | Python dependencies |
| `Beijing_Air_Quality_Activity2.pptx` | PowerPoint presentation |
| `charts/` | All generated charts (PNG) |

---

## Charts

| File | Description |
|---|---|
| `task4a_pm25_boxplot.png` | PM2.5 distribution by station |
| `task4b_pm25_monthly.png` | Monthly PM2.5 trend 2013–2017 |
| `task4c_pm25_hourly.png` | Average PM2.5 by hour of day |
| `task4d_pm25_season.png` | Average PM2.5 by season |
| `task4e_pm25_station_bar.png` | Mean PM2.5 per station |
| `task5a_correlation_heatmap.png` | Correlation heatmap |
| `task5b_pm25_vs_temp.png` | PM2.5 vs Temperature scatter |
| `task5c_pm25_vs_wspm.png` | PM2.5 vs Wind Speed scatter |

---

## How to Run

```bash
# 1. Download the dataset from UCI and extract CSV files into the same folder
#    https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality+data

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run full analysis (Tasks 1–6)
python analysis.py
```

Charts will be saved to a `charts/` folder automatically.

---

## Key Findings

- Mean PM2.5 across all stations: **79.27 µg/m³** — 15.9x the WHO annual guideline (5 µg/m³)
- Strongest correlation with PM2.5: **PM10 (r = 0.88)** and **CO (r = 0.77)**
- Wind speed reduces PM2.5 (r = −0.27) — primary natural dispersal mechanism
- Urban stations are 20–30% more polluted than suburban stations

---

## Citation

Chen, S. (2017). Beijing Multi-Site Air Quality [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5RK5G
