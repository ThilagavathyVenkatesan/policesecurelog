import pandas as pd

# Load the dataset safely
df = pd.read_csv(
    "C:/Users/Modern/Downloads/traffic_stops - traffic_stops_with_vehicle_number.csv",
    low_memory=False
)

# Drop rows missing critical fields
df.drop(columns=['driver_age_raw'], inplace=True)
df.dropna(subset=['stop_date', 'stop_time', 'driver_gender', 'driver_age', 'violation'], inplace=True)

# Convert types
df['stop_date'] = pd.to_datetime(df['stop_date'], errors='coerce').dt.date
df['stop_time'] = pd.to_datetime(df['stop_time'], format='%H:%M:%S', errors='coerce').dt.time
df['driver_age'] = pd.to_numeric(df['driver_age'], errors='coerce')
df['search_conducted'] = df['search_conducted'].astype(bool)
df['drugs_related_stop'] = df['drugs_related_stop'].astype(bool)


# Handle missing values safely
df['search_type'] = df['search_type'].fillna('')
df['country_name'] = df['country_name'].fillna('Unknown')
df['stop_duration'] = df['stop_duration'].fillna('0-15 Min')
df['stop_outcome'] = df['stop_outcome'].fillna('Warning')
df['vehicle_number'] = df['vehicle_number'].fillna('NA')

# Preview
print(df.head())

# Save cleaned version
df.to_csv("cleaned_traffic_data.csv", index=False)
