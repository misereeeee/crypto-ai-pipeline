import websocket
import json

# Binance WebSocket address for real-time Bitcoin to USD-Tether trades
SOCKET = "wss://stream.binance.com:9443/ws/btcusdt@trade"

def on_message(ws, message):
    """Runs every time a new message is received from Binance"""
    # The message comes in as a string of JSON data. We convert it to a Python dictionary.
    json_message = json.loads(message)
    
    # Extract the exact price from the dictionary (Binance calls price 'p')
    price = json_message['p']
    
    # Extract the trade time (Binance calls trade time 'T')
    trade_time = json_message['T']
    
    print(f"Bitcoin Price: ${price} (Timestamp: {trade_time})")

def on_error(ws, error):
    """Runs if something goes wrong"""
    print(f"Error occurred: {error}")

def on_close(ws, close_status_code, close_msg):
    """Runs when the connection is closed"""
    print("### Connection Closed ###")

def on_open(ws):
    """Runs the moment we successfully connect"""
    print("### Successfully Connected to Binance Stream ###")

# MAIN
if __name__ == "__main__":
    # Create the WebSocket application
    ws = websocket.WebSocketApp(SOCKET, 
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    
    # Run the WebSocket forever
    ws.run_forever()