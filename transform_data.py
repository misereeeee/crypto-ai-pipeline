import pandas as pd

print("Loading raw data...")
df = pd.read_csv('btc_price_data.csv')
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df.set_index('Timestamp', inplace=True)

print("Transforming data into 1-minute OHLC chunks...")
ohlc_data = df['Price'].resample('1min').ohlc()
ohlc_data.dropna(inplace=True)

print("Calculating Machine Learning Features and Target...")

# FEATURE 1: 3-Minute Simple Moving Average (SMA)
# This gives the AI the average closing price of the last 3 minutes
ohlc_data['SMA_3'] = ohlc_data['close'].rolling(window=3).mean()

# FEATURE 2: Price Return
# This tells the AI the percentage the price changed from the previous minute
ohlc_data['Return'] = ohlc_data['close'].pct_change()

# THE TARGET: Did the price go UP in the NEXT minute?
# We use .shift(-1) to look into the future. 
# If next minute's close > this minute's close, put a 1. Else, put a 0.
ohlc_data['Target'] = (ohlc_data['close'].shift(-1) > ohlc_data['close']).astype(int)

# Because Moving Averages need previous rows, and our Target needs future rows,
# the very first and very last rows will have missing data (NaN). We drop them.
ohlc_data.dropna(inplace=True)

# Save this ultimate AI-ready data to a new file
ohlc_data.to_csv('btc_ml_data.csv')

print("\nSuccess! Here is your Machine Learning dataset:")
print(ohlc_data[['close', 'SMA_3', 'Return', 'Target']].head())