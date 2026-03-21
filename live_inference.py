import websocket
import json
import joblib
import pandas as pd

# 1. Load the AI Brain into memory before connecting to the stream
print("Loading AI Brain...")
model = joblib.load('crypto_ai_brain.joblib')
print("AI Brain loaded successfully!")

SOCKET = "wss://stream.binance.com:9443/ws/btcusdt@trade"

# 2. Create a "Memory" (State) to hold the last few prices
price_history = []

def on_message(ws, message):
    global price_history  
    
    json_message = json.loads(message)
    current_price = float(json_message['p'])
    
    # Add the new price to our memory
    price_history.append(current_price)
    
    # We only want to keep the last 4 prices to save computer memory
    if len(price_history) > 4:
        price_history.pop(0) # Remove the oldest price
        
    # We need at least 3 prices in memory to calculate a 3-tick SMA!
    if len(price_history) >= 3:
        # Calculate SMA_3 (Average of the last 3 prices)
        sma_3 = sum(price_history[-3:]) / 3
        
        # Calculate Return (Percentage change from the previous price)
        previous_price = price_history[-2]
        price_return = (current_price - previous_price) / previous_price

        # Put the live features into a Pandas DataFrame so the AI recognizes the column names
        live_features = pd.DataFrame([[current_price, sma_3, price_return]], 
                                     columns=['close', 'SMA_3', 'Return'])

        # The AI returns a list of answers. We grab the first one [0]
        prediction = model.predict(live_features)[0] 
        
        # Translate the AI's 1 or 0 into human words
        if prediction == 1:
            ai_thought = "🟢 AI Predicts: UP"
        else:
            ai_thought = "🔴 AI Predicts: DOWN"
            
        print(f"Live Price: ${current_price:.2f} | {ai_thought}")
    else:
        print(f"Live Price: ${current_price:.2f} | ⏳ AI gathering data...")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("### Connection Closed ###")

def on_open(ws):
    print("### Connected to Live Stream. Starting Inference... ###")

if __name__ == "__main__":
    ws = websocket.WebSocketApp(SOCKET, 
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()