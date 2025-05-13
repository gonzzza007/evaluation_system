import pandas as pd
import sqlite3
import xml.etree.ElementTree as ET
from datetime import datetime

# Step 1: Extract from PHP Lite
conn = sqlite3.connect('your_data.db')
df_main = pd.read_sql_query("SELECT * FROM properties", conn)

# Step 2: Load additional XML info (for example, eraldis_id-based data)
# You’ll need a loop for matching XML to main df

# Step 3: Calculate derived values (e.g. transport cost, soil factors...)

# Step 4: Normalize fields (area, age, price etc.)
df['area_norm'] = (df['area'] - df['area'].min()) / (df['area'].max() - df['area'].min())

# Normalize dates
df['timestamp'] = pd.to_datetime(df['sale_date']).astype(int) / 10**9
df['timestamp_norm'] = (df['timestamp'] - df['timestamp'].min()) / (df['timestamp'].max() - df['timestamp'].min())

# Step 5: Save intermediate file
df.to_parquet("prepared_data.parquet")