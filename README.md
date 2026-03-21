# Real-Time Cryptocurrency Machine Learning Pipeline

## 🚀 Overview
This project is an end-to-end Data Engineering and Machine Learning pipeline. It streams high-frequency, real-time cryptocurrency tick data via WebSockets, performs ETL (Extract, Transform, Load) operations to create machine learning features, and serves a serialized AI model for low-latency live market predictions.

## 🏗️ Architecture & Pipeline
The system is divided into four distinct micro-components:

1. **Live Data Ingestion (`stream_data.py`)**
   - Connects to the Binance public WebSocket.
   - Captures high-frequency live trades (BTC/USDT) and translates Unix Epoch timestamps into human-readable formats.
   - Logs raw streaming data to a local CSV for historical storage.

2. **Data Transformation & Feature Engineering (`transform_data.py`)**
   - Utilizes **Pandas** to aggregate raw tick data into 1-minute OHLC (Open, High, Low, Close) candlesticks.
   - Engineers predictive features such as the 3-period Simple Moving Average (SMA_3) and percentage price returns.
   - Generates a binary target variable (`1` for upward price movement, `0` for downward) for model training.

3. **Machine Learning Training (`train_model.py`)**
   - Implements a **Random Forest Classifier** using **Scikit-Learn**.
   - Handles time-series data splitting correctly (preventing data leakage).
   - Serializes and exports the trained model state using `joblib` for production deployment.

4. **Real-Time AI Inference (`live_inference.py`)**
   - Loads the serialized machine learning model into memory.
   - Re-establishes the WebSocket connection to the live market.
   - Maintains a running state (memory) of the latest ticks to calculate live features on the fly.
   - Outputs sub-second AI predictions on future price trajectory based on live streaming data.

## 💻 Tech Stack
* **Language:** Python
* **Data Engineering:** Pandas, JSON, CSV handling, Datetime
* **Networking:** WebSockets (`websocket-client`)
* **Machine Learning:** Scikit-Learn (Random Forest), Joblib (Serialization)

## 🔮 Future Improvements
* Migrate local CSV storage to a Time-Series Database (e.g., PostgreSQL + TimescaleDB).
* Dockerize the application for cloud deployment (AWS EC2).
* Address *Training-Serving Skew* by buffering live WebSocket ticks into 1-minute batches before inference.