import websocket
import json
import csv
import os
from datetime import datetime  

# Binance WebSocket address
SOCKET = "wss://stream.binance.com:9443/ws/btcusdt@trade"
CSV_FILE = "btc_price_data.csv"

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Price"])

def on_message(ws, message):
    json_message = json.loads(message)
    price = json_message['p']
    
    # Raw Unix time in milliseconds
    trade_time_ms = json_message['T']
    
    # Convert the raw Unix time to a human-readable format
    readable_time = datetime.fromtimestamp(trade_time_ms / 1000.0).strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"Bitcoin Price: ${price} (Time: {readable_time})")
    
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Save the readable_time instead of the raw math number
        writer.writerow([readable_time, price]) 

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