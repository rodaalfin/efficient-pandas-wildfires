import sqlite3
import pandas as pd
import numpy as np

# 1. Connect and Load Data
conn = sqlite3.connect('FPA_FOD_20170508.sqlite') # Make sure this matches your filename
query = "SELECT FIRE_YEAR, STAT_CAUSE_DESCR, FIRE_SIZE, STATE, LATITUDE, LONGITUDE FROM Fires"

print("Reading from SQLite...")
df = pd.read_sql_query(query, conn)
conn.close()

def get_stats(df, label):
    usage_mb = df.memory_usage(deep=True).sum() / 1024**2
    print(f"--- {label} ---")
    print(f"Memory Usage: {usage_mb:.2f} MB")
    print(df.dtypes)
    print("-" * 20)
    return usage_mb

# --- AUDIT 1: RAW PANDAS LOAD ---
# This is how Pandas handles the data by default (heavy!)
before_mem = get_stats(df, "BEFORE OPTIMIZATION")

# --- STEP 2: THE "SUNAT" (OPTIMIZATION) ---

# A. Convert repetitive text to 'category'
# This is the biggest saver for columns like 'STATE' or 'STAT_CAUSE_DESCR'
for col in ['STATE', 'STAT_CAUSE_DESCR']:
    df[col] = df[col].astype('category')

# B. Downcast Numbers
# FIRE_YEAR doesn't need 64-bit! int16 is enough.
df['FIRE_YEAR'] = pd.to_numeric(df['FIRE_YEAR'], downcast='integer')
# Coordinates and Size can be float32 instead of float64
for col in ['FIRE_SIZE', 'LATITUDE', 'LONGITUDE']:
    df[col] = pd.to_numeric(df[col], downcast='float')

# --- AUDIT 2: AFTER OPTIMIZATION ---
after_mem = get_stats(df, "AFTER OPTIMIZATION")

# --- FINAL VERDICT ---
savings = 100 * (before_mem - after_mem) / before_mem
print(f"RESULTS: Memory reduced from {before_mem:.2f} MB to {after_mem:.2f} MB.")
print(f"Total RAM Savings: {savings:.2f}%")