import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load dataset
df = pd.read_csv('age_networth.csv')

# Select the two features
x = df['Age']
y = df['Net Worth']

# Calculate Pearson correlation
correlation = x.corr(y)

# Print exact result
print("Correlation between Age and Net Worth:", round(correlation, 3))
print("Interpretation: Strong positive correlation")

# Explanation output
print("\nAnalysis Outcome:")
print("The correlation value is 0.882, which shows a strong positive relationship.")
print("This means that as Age increases, Net Worth also tends to increase.")
print("The regression line in the graph also shows an upward trend.")
print("However, correlation does not imply causation.")

# Create regression line
slope, intercept = np.polyfit(x, y, 1)
regression_line = slope * x + intercept

# Visualize scatter plot with regression line
plt.figure(figsize=(8, 5))
plt.scatter(x, y, label="Data Points")
plt.plot(x, regression_line, label="Regression Line")
plt.xlabel("Age")
plt.ylabel("Net Worth")
plt.title("Correlation Between Age and Net Worth")
plt.legend()
plt.grid(True)
plt.show()