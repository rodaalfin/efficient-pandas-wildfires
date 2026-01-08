import sqlite3
import pandas as pd

def load_data(db_path):
    #conn = sqlite3.connect('FPA_FOD_20170508.sqlite')
    conn = sqlite3.connect(db_path)
    #query = "SELECT FIRE_YEAR, STAT_CAUSE_DESCR, FIRE_SIZE, STATE, LATITUDE, LONGITUDE FROM Fires"
    query = """
    SELECT 
        FIRE_YEAR, 
        STAT_CAUSE_DESCR, 
        FIRE_SIZE, 
        STATE, 
        LATITUDE, 
        LONGITUDE 
    FROM Fires
    """

    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def optimize_data(df):
    # Convert repetitive text to categories
    for col in ['STATE', 'STAT_CAUSE_DESCR']:
        df[col] = df[col].astype('category')
    
    # Downcast Year to smallest possible integer
    df['FIRE_YEAR'] = pd.to_numeric(df['FIRE_YEAR'], downcast='integer')
    
    # Downcast Floats (Size, Lat, Long) to float32
    for col in ['FIRE_SIZE', 'LATITUDE', 'LONGITUDE']:
        df[col] = pd.to_numeric(df[col], downcast='float')
        
    return df
  
if __name__ == "__main__":
    # 1. Load
    raw_df = load_data('FPA_FOD_20170508.sqlite')
    
    # 2. Audit Before
    mem_before = raw_df.memory_usage(deep=True).sum() / 1024**2
    
    # 3. Optimize
    df = optimize_data(raw_df)
    
    # 4. Audit After
    mem_after = df.memory_usage(deep=True).sum() / 1024**2
    print(f"Optimization Complete! Reduced from {mem_before:.2f}MB to {mem_after:.2f}MB")
    
    # 5. Save
    df.to_parquet('wildfires_clean.parquet')