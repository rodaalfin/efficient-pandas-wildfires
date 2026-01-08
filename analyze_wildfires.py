import pandas as pd

# Load the optimized Parquet file
df = pd.read_parquet('wildfires_clean.parquet')

print("--- DEEP DIVE ANALYSIS ---")

# 1. The "Danger" Metric: Which cause burns the most land?
# We sum the FIRE_SIZE for each cause
cause_impact = df.groupby('STAT_CAUSE_DESCR')['FIRE_SIZE'].sum().sort_values(ascending=False)

# 2. The "Efficiency" Metric: Which states are best at stopping fires while they are small?
# We look at the average fire size per state
avg_fire_size = df.groupby('STATE')['FIRE_SIZE'].mean().sort_values(ascending=True)

print("\nTop 5 Most Destructive Causes (Total Acres):")
print(cause_impact.head(5))

print("\nTop 5 States with the Smallest Average Fires (Fastest Response?):")
print(avg_fire_size.head(5))