import pandas as pd

print("Loading raw data...")
# Load raw data from CSV
df = pd.read_csv('btc_price_data.csv')

# Convert the Timestamp from string to a datetime object 
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Set Timestamp as the "Index" 
df.set_index('Timestamp', inplace=True)

print("Transforming data into 1-minute OHLC chunks...")
# Group data by 1-minute intervals ('1min') and calculate OHLC
# OHLC stands for Open, High, Low, Close
ohlc_data = df['Price'].resample('1min').ohlc()

# Remove any minutes that might be empty 
ohlc_data.dropna(inplace=True)

# Save the transformed data to a new CSV file
ohlc_data.to_csv('btc_1min_data.csv')

print("\nSuccess! Here is a preview of your transformed data:")
print(ohlc_data.head()) # Prints the first 5 rows to your screen