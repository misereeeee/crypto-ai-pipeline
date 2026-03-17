import websocket
import json
import csv
import os

# Binance WebSocket address
SOCKET = "wss://stream.binance.com:9443/ws/btcusdt@trade"

# File to save data
CSV_FILE = "btc_price_data.csv"

# Create CSV file if it doesn't exist and add headers
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Price"]) # Column names

def on_message(ws, message):
    """Runs every time we receive a new message"""
    json_message = json.loads(message)
    price = json_message['p']
    trade_time = json_message['T']
    
    print(f"Bitcoin Price: ${price} (Timestamp: {trade_time})")
    
    # Save the price and timestamp to the CSV file
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([trade_time, price]) # Save data

def on_error(ws, error):
    print(f"Error occurred: {error}")

def on_close(ws, close_status_code, close_msg):
    print("### Connection Closed ###")

def on_open(ws):
    print("### Successfully Connected to Binance Stream ###")

if __name__ == "__main__":
    ws = websocket.WebSocketApp(SOCKET, 
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()