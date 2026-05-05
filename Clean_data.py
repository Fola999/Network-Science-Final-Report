import pandas as pd

# Read CSV with header (uses first row as column names)
df = pd.read_csv('us_conflict_data_CLEAN_with_dates.csv', header=0)
df = df[['SQLDATE', 'Partner', 'QuadClass']].copy()  # Select your 3 columns

# Safe numeric conversion + filter
df['date_int'] = pd.to_numeric(df['SQLDATE'], errors='coerce')  # Bad values → NaN
df = df.dropna(subset=['date_int'])  # Remove bad rows
filtered_df = df[df['date_int'] >= 20260101].drop('date_int', axis=1)

# Save WITH headers
filtered_df.to_csv('filtered_data.csv', index=False, header=True)

print(f"✅ Filtered {len(df) - len(filtered_df)} rows → filtered_data.csv (WITH headers)")