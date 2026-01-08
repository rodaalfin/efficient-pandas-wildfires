import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load optimized data
df = pd.read_parquet('wildfires_clean.parquet')

# 2. Prepare Data: Count fires by cause
cause_counts = df['STAT_CAUSE_DESCR'].value_counts()

# 3. Set the professional style
sns.set_theme(style="whitegrid")
plt.figure(figsize=(12, 8))

# 4. Create Horizontal Bar Chart
plot = sns.barplot(
    x=cause_counts.values, 
    y=cause_counts.index, 
    palette="magma"
)

# 5. Add Titles and Labels
plt.title('Distribution of Wildfire Causes (1.88M Records)', fontsize=18, pad=20)
plt.xlabel('Number of Incidents', fontsize=14)
plt.ylabel('Cause', fontsize=14)

# 6. Add "The Pro Touch": Value labels on the bars
for i, v in enumerate(cause_counts.values):
    plot.text(v + 1000, i, f'{v:,}', color='black', va='center', fontsize=11)

# 7. Save it
plt.tight_layout()
plt.savefig('fire_causes_distribution.png', dpi=300)
print("✅ Visualization saved as fire_causes_distribution.png")